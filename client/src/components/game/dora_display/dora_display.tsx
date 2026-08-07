import { Tile2D, Tile2DBack } from "../tile_2d/tile_2d";
import type { TileId } from "../../../types/tile";

import "./dora_display.css";

export function DoraDisplay({
  dora,
  max_dora_count
}: {
  dora: TileId[];
  max_dora_count: number;
}) {
  if (max_dora_count == 0) {
    return <></>;
  }
  const tiles = dora.map((tile) => <Tile2D tile={tile} />);
  while (tiles.length < max_dora_count) {
    tiles.push(<Tile2DBack />);
  }
  return (
    <div class="dora_display">
      <div class="dora_title">Dora</div>
      <div class="tiles">
        {tiles}
      </div>
    </div>
  );
}
