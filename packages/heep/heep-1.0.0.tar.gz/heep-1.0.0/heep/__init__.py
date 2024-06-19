# Copyright (c) 2024 Khiat Mohammed Abderrezzak
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Author: Khiat Mohammed Abderrezzak <khiat.abderrezzak@gmail.com>


"""Sophisticate Heap"""


__all__: list = ["minBinaryHeap", "maxBinaryHeap"]


from tabulate import tabulate


def _blue(text: str) -> str:
    """Blue Coloring Function"""
    return f"\033[94;1m{text}\033[00m"


def _cyan(text: str) -> str:
    """Cyan Coloring Function"""
    return f"\033[36;1m{text}\033[00m"


def _white(text: str) -> str:
    """White Coloring Function"""
    return f"\033[37;1m{text}\033[00m"


class _binaryHeap:
    def __init__(self: "_binaryHeap", data: list, *, detail: bool = False) -> None:
        self.data: list = data
        self.detail: bool = detail

    def __len__(self: "_binaryHeap") -> int:
        return len(self._data)

    def __str__(self: "_binaryHeap") -> str:
        if not self.detail:
            return f"{self._data}"
        else:
            if self._data:
                items: list = [
                    [
                        _white("Current node"),
                        _white("Left child"),
                        _white("Right child"),
                    ]
                ]
            for i in range(len(self._data)):
                current = _blue(f"{self._data[i]}")
                try:
                    left = _blue(f"{self._data[(i * 2) + 1]}")
                except IndexError as e0:
                    left = _cyan("None")
                try:
                    right = _blue(f"{self._data[(i * 2) + 2]}")
                except IndexError as e1:
                    right = _cyan("None")
                items.append([current, left, right])
            return tabulate(items, headers="firstrow", tablefmt="fancy_grid")


class minBinaryHeap(_binaryHeap):
    @property
    def data(self: "minBinaryHeap") -> _binaryHeap:
        return self

    @data.setter
    def data(self: "minBinaryHeap", data: list) -> None:
        if not isinstance(data, list):
            raise TypeError("Just list data type accepted !")
        else:
            for i in range((len(data) // 2) - 1, -1, -1):
                while True:
                    current: int = i
                    left: int = (i * 2) + 1
                    right: int = (i * 2) + 2
                    if left < len(data) and data[left] < data[current]:
                        current: int = left
                    if right < len(data) and data[right] < data[current]:
                        current: int = right
                    if current != i:
                        data[i], data[current] = data[current], data[i]
                        i: int = current
                    else:
                        break
            self._data: list = data

    def get_min(self: "minBinaryHeap") -> object:
        if self._data:
            return self._data[0]

    def extract_min(self: "minBinaryHeap") -> object:
        if self._data:
            self._data[0], self._data[-1] = self._data[-1], self._data[0]
            extracted_value: object = self._data.pop()
            i: int = 0
            while True:
                current: int = i
                left: int = (i * 2) + 1
                right: int = (i * 2) + 2
                if left < len(self._data) and self._data[left] < self._data[current]:
                    current: int = left
                if right < len(self._data) and self._data[right] < self._data[current]:
                    current: int = right
                if current != i:
                    self._data[current], self._data[i] = (
                        self._data[i],
                        self._data[current],
                    )
                    i: int = current
                else:
                    break
            return extracted_value

    def add(self: "minBinaryHeap", value: object) -> None:
        self._data.append(value)
        i: int = len(self._data) - 1
        while i != 0:
            parent: int = (i - 1) // 2
            if self._data[parent] > self._data[i]:
                self._data[parent], self._data[i] = (
                    self._data[i],
                    self._data[parent],
                )
                i: int = parent
            else:
                break


class maxBinaryHeap(_binaryHeap):
    @property
    def data(self: "minBinaryHeap") -> _binaryHeap:
        return self

    @data.setter
    def data(self: "maxBinaryHeap", data: list) -> None:
        if not isinstance(data, list):
            raise TypeError("Just list data type accepted !")
        else:
            for i in range((len(data) // 2) - 1, -1, -1):
                while True:
                    current: int = i
                    left: int = (i * 2) + 1
                    right: int = (i * 2) + 2
                    if left < len(data) and data[left] > data[current]:
                        current: int = left
                    if right < len(data) and data[right] > data[current]:
                        current: int = right
                    if current != i:
                        data[i], data[current] = data[current], data[i]
                        i: int = current
                    else:
                        break
            self._data: list = data

    def get_max(self: "maxBinaryHeap") -> object:
        if self._data:
            return self._data[0]

    def extract_max(self: "maxBinaryHeap") -> object:
        if self._data:
            self._data[0], self._data[-1] = self._data[-1], self._data[0]
            extracted_value = self._data.pop()
            i = 0
            while True:
                current = i
                left = (i * 2) + 1
                right = (i * 2) + 2
                if left < len(self._data) and self._data[left] > self._data[current]:
                    current = left
                if right < len(self._data) and self._data[right] > self._data[current]:
                    current = right
                if current != i:
                    self._data[current], self._data[i] = (
                        self._data[i],
                        self._data[current],
                    )
                    i = current
                else:
                    break
            return extracted_value

    def add(self: "maxBinaryHeap", value: object) -> None:
        self._data.append(value)
        i: int = len(self._data) - 1
        while i != 0:
            parent: int = (i - 1) // 2
            if self._data[parent] < self._data[i]:
                self._data[parent], self._data[i] = (
                    self._data[i],
                    self._data[parent],
                )
                i: int = parent
            else:
                break


def _main():
    print("heep")


if __name__ == "__main__":
    _main()
