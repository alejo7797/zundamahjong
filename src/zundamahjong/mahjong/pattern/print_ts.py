# import to register patterns
from zundamahjong.mahjong.pattern.pattern_calculator import pattern_descs

typesBefore = """export type PatternData = {
  yaku: number;
  dora: number;
  fu: number;
};

type PatternDesc = {
  displayName: string;
  description: string;
};
"""

typesAfter = """export type Pattern = (typeof patterns)[number];

export type PatternDataDict = {
  [pattern in Pattern]: PatternData;
};
"""


if __name__ == "__main__":
    print(typesBefore)
    print(
        "export const patterns = [",
        "\n".join(f'  "{key}",' for key in pattern_descs),
        "] as const;\n",
        sep="\n",
    )
    print(
        "export const patternDescs: {",
        "  [pattern in Pattern]: PatternDesc;",
        "} = {",
        "\n".join(
            f'  {key}: {{\n    displayName: "{value.display_name}",\n    description: "{value.description}",\n  }},'
            for key, value in pattern_descs.items()
        ),
        "} as const;\n",
        sep="\n",
    )
    print(typesAfter, end="")
