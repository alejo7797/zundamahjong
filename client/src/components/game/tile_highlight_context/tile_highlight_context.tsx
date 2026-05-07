import { createContext } from "preact";
import type { TileValue } from "../../../types/tile";

type TileHighlight = {
  hoverTileValue: TileValue;
//   setHoverTileValue: (tile: TileValue) => void;
};

export const TileHighlightContext = createContext<TileHighlight>({
  hoverTileValue: 0,
//   setHoverTileValue: () => {},
});
