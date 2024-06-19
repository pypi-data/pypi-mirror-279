from .types import CompareHypothesisResult, HypothesisResult


class IsUniformResult(HypothesisResult):
    def __str__(self):
        return "Distribution is uniform" if self.value else "Distribution is not uniform"


class IsPoissonResult(HypothesisResult):
    def __str__(self):
        return "Distribution is poisson" if self.value else "Distribution is not poisson"


class VariationResult(CompareHypothesisResult):
    def _str_both(self):
        return "Variation is " + ("equal to" if self.value else "not equal to") + f" {self.part2}"

    def _str_left(self):
        return "Variation is " + ("equal to" if self.value else "less than") + f" {self.part2}"

    def _str_right(self):
        return "Variation is " + ("equal to" if self.value else "more than") + f" {self.part2}"


class DifferenceResult(CompareHypothesisResult):
    def _str_both(self):
        return "Mean difference is " + ("equal to" if self.value else "not equal to") + f" {self.part2}"

    def _str_left(self):
        return "Mean difference is " + ("equal to" if self.value else "less than") + f" {self.part2}"

    def _str_right(self):
        return "Mean difference is " + ("equal to" if self.value else "more than") + f" {self.part2}"


class MeanResult(CompareHypothesisResult):
    def _str_both(self):
        return "Mean is " + ("equal to" if self.value else "not equal to") + f" {self.part2}"

    def _str_left(self):
        return "Mean is " + ("equal to" if self.value else "less than") + f" {self.part2}"

    def _str_right(self):
        return "Mean is " + ("equal to" if self.value else "more than") + f" {self.part2}"


class CompareMeanResult(CompareHypothesisResult):
    def _str_both(self):
        return f"Mean of first ({self.part1}) is " + (
            "equal to" if self.value else "not equal to") + f" mean of second ({self.part2})"

    def _str_left(self):
        return f"Mean of first ({self.part1}) is " + (
            "equal to" if self.value else "less than") + f" mean of second ({self.part2})"

    def _str_right(self):
        return f"Mean of first ({self.part1}) is " + (
            "equal to" if self.value else "more than") + f" mean of second ({self.part2})"
