# SPDX-License-Identifier: BSD-3-Clause

from typing import Optional, Tuple

import numpy as np
from patterns import quad, glider, gun, replicator, p2

from cholerama import Positions, helpers

AUTHOR = "ItsAlwaysSunny"  # This is your team name
SEED = None  # Set this to a value to make runs reproducible


class Bot:
    """
    This is the bot that will be instantiated for the competition.

    The pattern can be either a numpy array or a path to an image (white means 0,
    black means 1).
    """

    def __init__(
            self,
            number: int,
            name: str,
            patch_location: Tuple[int, int],
            patch_size: Tuple[int, int],
    ):
        """
        Parameters:
        ----------
        number: int
            The player number. Numbers on the board equal to this value mark your cells.
        name: str
            The player's name
        patch_location: tuple
            The i, j row and column indices of the patch in the grid
        patch_size: tuple
            The size of the patch
        """
        self.number = number  # Mandatory: this is your number on the board
        self.name = name  # Mandatory: player name
        self.color = None  # Optional
        self.patch_location = patch_location
        self.patch_size = patch_size
        self.first_run = True

        self.rng = np.random.default_rng(SEED)

        # If we make the pattern too sparse, it just dies quickly
        xy = self.rng.integers(0, 50, size=(2,))
        #self.pattern = Positions(
        #    x=xy[1] + patch_size[1] // 2, y=xy[0] + patch_size[0] // 2
        #)

        x, y = np.where(p2 == 1)
        x1, y1 = np.where(np.rot90(p2) == 1)
        x2, y2 = np.where(np.rot90(np.rot90(p2)) == 1)
        # x3, y3 = np.where(np.rot90(np.rot90(np.rot90(p2))) == 1)

        self.pattern = Positions(
            x=np.concatenate([
                xy[1] + y,
                -1*(xy[1] + y1) + patch_size[1],
                xy[1] + y2,
                #-1*(xy[1] + y3) + patch_size[1]
            ]),
            y=np.concatenate([
                xy[0] + x,
                -1*(xy[0] + x1) + patch_size[0],
                -1*(xy[0] + x2) + patch_size[0],
                #xy[0] + x3
            ])
        )
        # The pattern can also be just an image (0=white, 1=black)
        # self.pattern = "mypattern.png"

    def iterate(
            self, iteration: int, board: np.ndarray, patch: np.ndarray, tokens: int
    ) -> Optional[Positions]:
        """
        This method will be called by the game engine on each iteration.

        Parameters:
        ----------
        iteration : int
            The current iteration number.
        board : numpy array
            The current state of the entire board.
        patch : numpy array
            The current state of the player's own patch on the board.
        tokens : list
            The list of tokens on the board.

        Returns:
        -------
        An object containing the x and y coordinates of the new cells.
        """
        # if iteration > 600 & iteration < 600 + np.sum(gun):
        #     return self.create_gun(tokens, patch)

        pattern = None
        if self.first_run:
            if tokens < np.sum(gun):
                return pattern
            else:
                self.first_run = False

        if tokens >= np.sum(gun):
            pattern = self.create_gun(tokens, patch)
            if pattern is None:
                pattern = self.create_glider(tokens, patch)
        else:
            if tokens >= np.sum(glider['NE']):
                pattern = self.create_glider(tokens, patch)
        return pattern

    def create_glider(self, tokens, patch):
        direction = list(glider.keys())
        selected_glider = glider[direction[self.rng.integers(0, len(direction))]]
        if tokens >= np.sum(selected_glider):
            # Pick a random empty region of size 3x3 inside my patch
            empty_regions = helpers.find_empty_regions(patch, (5, 5))
            nregions = len(empty_regions)
            if nregions == 0:
                return None
        ind = self.rng.integers(0, nregions)
        x, y = np.where(selected_glider == 1)
        pattern = Positions(x=empty_regions[ind, 1] + x, y=empty_regions[ind, 0] + y)
        return pattern

    def create_gun(self, tokens, patch):
        this_gun = gun.copy()
        if tokens >= np.sum(gun):
            # Pick a random empty region of size 3x3 inside my patch
            empty_regions = helpers.find_empty_regions(patch, (3, 49))
            nregions = len(empty_regions)
            if nregions == 0:
                this_gun = np.transpose(this_gun)
                empty_regions = helpers.find_empty_regions(patch, (49, 3))
                nregions = len(empty_regions)
                if nregions == 0:
                    return None
        else:
            return None
        ind = self.rng.integers(0, nregions)
        x, y = np.where(this_gun == 1)
        pattern = Positions(x=empty_regions[ind, 1] + x, y=empty_regions[ind, 0] + y)
        return pattern
