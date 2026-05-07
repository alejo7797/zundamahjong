import { useContext } from "preact/hooks";
import { getTileValue, type TileId } from "../../../types/tile";

import { TileImage } from "../tile_image/tile_image";

import "./tile_3d.css";
import { TileHighlightContext } from "../tile_highlight_context/tile_highlight_context";

export function Tile3D({
  tile,
  is_new,
  is_called,
  is_added_kan,
  is_closed_kan,
  isFirstRiichi,
}: {
  tile: TileId;
  is_new?: boolean;
  is_called?: boolean;
  is_added_kan?: boolean;
  is_closed_kan?: boolean;
  isFirstRiichi?: boolean;
}) {
  const tileHighlight = useContext(TileHighlightContext);
  return (
    <div
      class={`tile_3d tile_id_${tile} ${is_new ? "is_new " : ""}${
        is_called ? "is_called " : ""
      }${is_added_kan ? "is_added_kan " : ""}${
        is_closed_kan ? "is_closed_kan " : ""
      }${isFirstRiichi ? "is_first_riichi " : ""}${
        tile && getTileValue(tile) == tileHighlight.hoverTileValue
          ? "is_hover_highlight "
          : ""
      }`}
    >
      <div class={`tile_3d_extra_transform`}>
        <span class="tile_face tile_back" />
        <span class="tile_face tile_left" />
        <span class="tile_face tile_right" />
        <span class="tile_face tile_top" />
        <span class="tile_face tile_bottom" />
        <span class="tile_face tile_front">
          <TileImage tile={tile} />
        </span>
      </div>
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
