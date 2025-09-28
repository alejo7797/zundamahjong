import type { TileId } from "../../../types/tile";

import { TileImage } from "../tile_image/tile_image";

import "./tile_3d.css";

export function Tile3D({ tile }: { tile: TileId }) {
  return (
    <div class={`tile_3d tile_id_${tile}`}>
      <span class="tile_face tile_back" />
      <span class="tile_face tile_left" />
      <span class="tile_face tile_right" />
      <span class="tile_face tile_top" />
      <span class="tile_face tile_bottom" />
      <span class="tile_face tile_front">
        <TileImage tile={tile} />
      </span>
    </div>
  );
}

export function Tile3DList({ tiles }: { tiles: ReadonlyArray<TileId> }) {
  return (
    <>
      {tiles.map((tile) => (
        <Tile3D key={tile} tile={tile} />
      ))}
    </>
  );
}
