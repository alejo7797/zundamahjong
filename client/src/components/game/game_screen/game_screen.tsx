import { useContext, useEffect, useLayoutEffect, useState } from "preact/hooks";

import type { AvatarIdDict } from "../../../types/avatars";
import {
  ActionType,
  type Action,
  type HandTileActionType,
} from "../../../types/action";
import {
  RoundStatus,
  type HistoryItem,
  type EnhancedGameInfo,
} from "../../../types/game";
import { type Player } from "../../../types/player";

import { Emitter } from "../../emitter/emitter";
import { EmitAction } from "../emit_action/emit_action";

import { PlayerIcons } from "../player_icon/player_icon";
import { Hand } from "../hand/hand";
import { DoraDisplay } from "../dora_display/dora_display.tsx";
import { ActionMenu } from "../action_menu/action_menu";
import { Table } from "../table/table";
import { WinInfo } from "../win_info/win_info";
import { Results } from "../results/results";

import { setAnimations } from "./animations";

import "./game_screen.css";
import {
  ShantenDisplay,
  ShantenDisplayButton,
} from "../shanten_display/shanten_display";
import { getTileValue, type TileId } from "../../../types/tile";
import { VoiceCollection } from "../../audio_collection/audio_collection";
import { CutinCollection } from "../cutin/cutin";
import { OptionsBar } from "../options_bar/options_bar";
import { OptionsContext } from "../../options_context/options_context";
import { TileHighlightContext } from "../tile_highlight_context/tile_highlight_context";
import { DoraContext, getDoraValues } from "../dora_context/dora_context.tsx";

export function GameScreen({
  playerAvatarIds,
  players,
  info,
  historyUpdates,
  actionSubmitted,
  setActionSubmitted,
  seeResults,
  goToResults,
}: {
  playerAvatarIds: AvatarIdDict;
  players: Player[];
  info: EnhancedGameInfo;
  historyUpdates: HistoryItem[];
  actionSubmitted: boolean;
  setActionSubmitted: () => void;
  seeResults: boolean;
  goToResults: () => void;
}) {
  const [hoverTile, setHoverTile] = useState<TileId | null>(null);
  const [handActionType, setHandActionType] = useState<HandTileActionType>(
    ActionType.DISCARD,
  );

  const emit = useContext(Emitter);
  const emit_action = (action: Action) => {
    setActionSubmitted();
    emit("action", action, info.round_info.history.length);
  };

  const options = useContext(OptionsContext)!;

  useEffect(() => {
    if (info.round_info.current_player == info.player_index) {
      if (info.round_info.status == RoundStatus.START) {
        setHandActionType(ActionType.FLOWER);
      } else {
        setHandActionType(ActionType.DISCARD);
      }
    } else {
      setHandActionType(ActionType.DISCARD);
    }
  }, [info]);

  useLayoutEffect(() => {
    // calculate this inside to avoid triggering this effect every time
    // this component is rerendered
    const avatarIds = players.map(
      (player) => playerAvatarIds[player.id],
    );
    setAnimations(historyUpdates, avatarIds);
  }, [players, historyUpdates, playerAvatarIds]);

  const avatarIds = players.map(
    (player) => playerAvatarIds[player.id],
  );
  const voiceCollections = [...new Set(Object.values(playerAvatarIds))].map(
    (avatarId) => <VoiceCollection key={avatarId} avatarId={avatarId} />,
  );

  const winOverlay =
    info.round_info.status != RoundStatus.END ? (
      <></>
    ) : !seeResults ? (
      <WinInfo
        players={players}
        playerAvatarIds={playerAvatarIds}
        info={info}
        goToResults={goToResults}
      />
    ) : (
      <Results
        players={players}
        playerAvatarIds={playerAvatarIds}
        info={info}
      />
    );

  function didDrawTile(info: EnhancedGameInfo) {
    if (info.round_info.current_player != info.player_index) {
      return false;
    }
    if (
      info.round_info.history.every(
        (historyItem) =>
          historyItem.action.action_type == ActionType.FLOWER ||
          historyItem.action.action_type == ActionType.CONTINUE,
      )
    ) {
      return false;
    }
    const lastHistoryItem = info.round_info.history.at(-1);
    if (!lastHistoryItem) {
      return false;
    }
    const lastActionType = lastHistoryItem.action.action_type;
    const isDrawActionType = {
      [ActionType.PASS]: false,
      [ActionType.CONTINUE]: true,
      [ActionType.DRAW]: true,
      [ActionType.DISCARD]: false,
      [ActionType.RIICHI]: false,
      [ActionType.CHII]: false,
      [ActionType.PON]: false,
      [ActionType.OPEN_KAN]: true,
      [ActionType.ADD_KAN]: true,
      [ActionType.CLOSED_KAN]: true,
      [ActionType.FLOWER]: true,
      [ActionType.RON]: true,
      [ActionType.TSUMO]: false,
    } as const;
    return isDrawActionType[lastActionType];
  }
  const discard_shanten_info =
    info.player_info.discard_shanten_info &&
    hoverTile &&
    info.player_info.discard_shanten_info[hoverTile];

  const tileHighlight = {
    hoverTileValue: hoverTile ? getTileValue(hoverTile) : 0,
  };

  const max_dora_count = Math.max(
    Math.min(
      options.game_options.max_dora_count,
      options.game_options.max_kan_count + options.game_options.start_dora_count,
    ),
    options.game_options.start_dora_count,
  );


  return (
    <EmitAction.Provider value={emit_action}>
      <DoraContext value={getDoraValues(info.round_info.dora, info.player_count == 3)}>
      <TileHighlightContext value={tileHighlight}>
        <div
          class={`screen game_screen me_player_${info.player_index} status_${info.round_info.status} show_tile_names_${options.client_options.show_tile_numbers ? "true" : "false"}`}
        >
          {voiceCollections}
          <CutinCollection
            historyUpdates={historyUpdates}
            avatarIds={avatarIds}
          />
          <PlayerIcons
            players={players}
            playerAvatarIds={playerAvatarIds}
          />
          <Hand
            handActionType={handActionType}
            tiles={info.player_info.hand}
            didDrawTile={didDrawTile(info)}
            actions={info.player_info.actions}
            actionSubmitted={actionSubmitted}
            isFuriten={info.player_info.is_furiten}
            setHoverTile={setHoverTile}
          />
          <DoraDisplay
            dora={info.round_info.dora}
            max_dora_count={max_dora_count}
          />
          {actionSubmitted ? (
            <></>
          ) : (
            <ActionMenu
              actions={info.player_info.actions}
              handActionType={handActionType}
              setHandActionType={setHandActionType}
            />
          )}
          {info.player_info.shanten_info ? (
            <ShantenDisplayButton
              shantenInfo={info.player_info.shanten_info}
              remainingTileCounts={info.player_info.remaining_tile_counts}
            />
          ) : (
            <></>
          )}
          {discard_shanten_info ? (
            <ShantenDisplay
              shantenInfo={discard_shanten_info}
              remainingTileCounts={info.player_info.remaining_tile_counts}
              visible
            />
          ) : (
            <></>
          )}
          <Table info={info} />
          {winOverlay}
          <OptionsBar />
        </div>
      </TileHighlightContext>
      </DoraContext>
    </EmitAction.Provider>
  );
}
