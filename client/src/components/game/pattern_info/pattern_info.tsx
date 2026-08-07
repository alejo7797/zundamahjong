import type { JSX } from "preact/jsx-runtime";
import { patternDescs, type Pattern, type PatternData } from "../../../types/pattern";
import "./pattern_info.css";

export function PatternInfo({ pattern, data }: { pattern: Pattern, data: PatternData }) {
  const children: JSX.Element[] = [];
  if (data.han != 0) {
    children.push(<span class="han">{`${data.han} han`}</span>);
  }
  if (data.fu != 0) {
    children.push(<span class="fu">{`${data.fu} fu`}</span>);
  }
  return (
    <div class="pattern">
      <span class="display_name">{patternDescs[pattern].displayName}</span>
      <span class="values">{children}</span>
    </div>
  );
}
