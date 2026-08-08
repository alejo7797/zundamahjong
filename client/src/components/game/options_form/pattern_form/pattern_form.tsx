import { type PatternDataDict, patterns } from "../../../../types/pattern";
import { GameOptionsPatternInput } from "./pattern_input";

import "./pattern_form.css";

export function PatternForm({
  patternValues,
  patternFormId,
  isEditable,
  sendGameOptions,
}: {
  patternValues: PatternDataDict;
  patternFormId: string;
  isEditable: boolean;
  sendGameOptions: () => void;
}) {
  return (
    <details class="pattern_options">
      <summary>Patterns</summary>
      <div class="table_header">
        <div>Pattern</div>
        <div>Yaku</div>
        <div>Dora</div>
        <div>Fu</div>
      </div>
      {patterns.map((pattern) => (
        <GameOptionsPatternInput
          key={pattern}
          isEditable={isEditable}
          name={pattern}
          data={patternValues[pattern]}
          formId={patternFormId}
          sendGameOptions={sendGameOptions}
        />
      ))}
    </details>
  );
}

export function getPatternDataDict(patternFormId: string): PatternDataDict {
  const patternFormData = new FormData(
    document.getElementById(patternFormId) as HTMLFormElement,
  );
  return Object.fromEntries(
    patterns.map((pattern) => [
      pattern,
      {
        yaku: Number(patternFormData.get(`${pattern}___yaku`)),
        dora: Number(patternFormData.get(`${pattern}___dora`)),
        fu: Number(patternFormData.get(`${pattern}___fu`)),
      },
    ]),
  ) as PatternDataDict;
}
