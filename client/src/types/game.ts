import type { TileId, TileValue } from "./tile.ts";
import type { Call } from "./call.ts";
import type { Action } from "./action.ts";
import type { Player } from "./player.ts";
import type { PatternData } from "./pattern.ts";

export type Discard = {
  player: number;
  tile: TileId;
  is_new: boolean;
  is_called: boolean;
  is_added_kan: boolean;
  is_closed_kan: boolean;
};

export type HistoryItem = {
  player_index: number;
  action: Action;
};

export const enum RoundStatus {
  START = 0,
  PLAY = 1,
  CALLED_PLAY = 2,
  ADD_KAN_AFTER = 3,
  CLOSED_KAN_AFTER = 4,
  DISCARDED = 5,
  LAST_DISCARDED = 6,
  END = 7,
}

export type GameInfo = {
  wind_round: number;
  sub_round: number;
  draw_count: number;
  player_scores: number[];
};

export type RoundInfo = {
  tiles_left: number;
  current_player: number;
  status: RoundStatus;
  discards: Discard[];
  history: HistoryItem[];
  hand_counts: number[];
  riichi_discard_indexes: (number | null)[];
  calls: Call[][];
  flowers: TileId[][];
  dora: TileId[];
};

export type PlayerInfo = {
  hand: TileId[];
  actions: Action[];
  is_furiten: boolean;
};

export type Win = {
  win_player: number;
  lose_player: number | null;
  hand: TileId[];
  calls: Call[];
  flowers: TileId[];
};

export type Scoring = {
  win_player: number;
  lose_player: number | null;
  patterns: { [pattern: string]: PatternData };
  han: number;
  fu: number;
  player_scores: number[];
};

export type AllGameInfo = {
  player_count: number;
  player_index: number;
  is_game_end: boolean;
  game_info: GameInfo;
  round_info: RoundInfo;
  player_info: PlayerInfo;
  win_info: Win | null;
  scoring_info: Scoring | null;
};

export type EnhancedGameInfo = AllGameInfo & {
  player_info: {
    shanten_info?: [number, Set<TileValue>];
    discard_shanten_info?: {
      [tile in TileId]?: [number, Set<TileValue>];
    };
    remaining_tile_counts: number[];
  };
}

export type AllServerInfo = {
  all_game_info: AllGameInfo;
  players: Player[];
  history_updates: HistoryItem[];
}

export type EnhancedInfo = AllServerInfo & {
  all_game_info: EnhancedGameInfo;
}
