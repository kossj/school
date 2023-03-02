from typing import List, Tuple

def scaleGenerator(key: str, permute: str) -> Tuple[str, List[str]]:
    notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"] 

    major_indices = [0, 2, 4, 5, 7, 9, 11]
    minor_indices = [0, 2, 3, 5, 7, 8, 10]

    if not (key.upper() in notes and permute.lower() in ["major", "minor"]):
        return -1

    if permute.lower() == "major":
        permutation = major_indices
    else:
        permutation = minor_indices

    mod = notes.index(key.upper())

    chromatic_scale = [notes[(idx + mod) % (len(notes))] for idx in range(len(notes))]

    scale = [note for (idx, note) in enumerate(chromatic_scale) if idx in permutation]
    scale.append(scale[0])

    name = f"{key.upper()} {permute.lower()}"
    return tuple((name, scale))


if __name__=="__main__":
    scale_call = scaleGenerator('G#', 'minor')
    print(f"{scale_call[0]}:\n{' '.join(scale_call[1])}")

