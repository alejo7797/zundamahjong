from zundamahjong.mahjong.pattern import default_pattern_data

typesBefore = """export type PatternData = {
  display_name: string;
  han: number;
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
        f"export const patterns = [",
        "\n".join(f'  "{key}",' for key in default_pattern_data),
        "] as const;\n",
        sep="\n",
    )
    print(
        "export const patternDescs: {",
        "  [pattern in Pattern]: PatternDesc;",
        "} = {",
        "\n".join(
            f'  {key}: {{\n    displayName: "{value.display_name}",\n    description: "{value.description}"\n  }},'
            for key, value in default_pattern_data.items()
        ),
        "} as const;\n",
        sep="\n",
    )
    print(typesAfter, end="")
