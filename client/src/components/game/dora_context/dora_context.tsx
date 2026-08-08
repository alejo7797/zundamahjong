import { createContext } from "preact";
import { getTileValue, type TileValue, type TileId } from "../../../types/tile";

export const DoraContext = createContext<TileValue[]>([]);

function getDoraValue(tile: TileId, is_3player: boolean): TileValue {
  const value = getTileValue(tile);
  if (is_3player && value === 1) return 9;
  if (value < 30 && value % 10 === 9) return (value - 8) as TileValue;
  if (value === 34) return 31;
  if (value === 37) return 35;
  return (value + 1) as TileValue;
}

function getDoraFlowerValues(tile: TileId): TileValue[] {
  console.log(tile);
  const value = getTileValue(tile);
  if (value <= 44) return [41, 42, 43, 44];
  return [45, 46, 47, 48];
}

export function getDoraValues(
  dora_ids: TileId[],
  is_3player: boolean,
): TileValue[] {
  const dora: TileValue[] = [];
  for (const tile of dora_ids) {
    if (getTileValue(tile) < 40) {
      dora.push(getDoraValue(tile, is_3player));
    } else {
      dora.push(...getDoraFlowerValues(tile));
    }
  }
  return dora;
}

export function isDora(tile: TileId, dora: TileValue[]): boolean {
  return dora.includes(getTileValue(tile));
}
