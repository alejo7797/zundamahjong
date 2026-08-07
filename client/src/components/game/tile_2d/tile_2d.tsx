import { useContext } from "preact/hooks";

import type { TileId } from "../../../types/tile";
import { DoraContext, isDora } from "../dora_context/dora_context.tsx";

import { TileImage } from "../tile_image/tile_image";

import "./tile_2d.css";

export function Tile2D({ tile }: { tile: TileId }) {
  const dora = useContext(DoraContext);
  return (
    <span class={`tile_div tile_2d tile_2d_front ${isDora(tile, dora) ? "is_dora ": ""}`}>
      <div class="tile_back_layer" />
      <div class="tile_middle_layer" />
      <TileImage tile={tile} />
    </span>
  );
}

export function Tile2DBack() {
  return (
    <span class="tile_div tile_2d tile_2d_back">
      <div class="tile_back_layer" />
      <div class="tile_middle_layer" />
      <div class="tile_front_layer" />
    </span>
  );
}

export function Tile2DList({ tiles }: { tiles: ReadonlyArray<TileId> }) {
  return (
    <>
      {tiles.map((tile) => (
        <Tile2D key={tile} tile={tile} />
      ))}
    </>
  );
}
