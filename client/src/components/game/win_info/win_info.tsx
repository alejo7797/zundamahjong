import { avatars, type AvatarIdDict } from "../../../types/avatars";
import type { Player } from "../../../types/player";
import type { AllGameInfo } from "../../../types/game";

import { Tile2D, Tile2DBack } from "../tile_2d/tile_2d";
import { WinHand } from "../win_hand/win_hand";
import { PatternInfo } from "../pattern_info/pattern_info";
import { WinTotalScore } from "../win_total_score/win_total_score";

import "./win_info.css";

export function WinInfo({
  players,
  playerAvatarIds,
  info,
  goToResults,
}: {
  players: ReadonlyArray<Player>;
  playerAvatarIds: AvatarIdDict;
  info: AllGameInfo;
  goToResults: () => void;
}) {
  let winInfoInner = <></>;
  if (info.scoring_info) {
    const winnerAvatar =
      avatars[playerAvatarIds[players[info.scoring_info.win_player].id]];
    const dora_tiles = info.scoring_info.dora_tiles.map((tile, index) => tile ? <Tile2D tile={tile} key={tile}/> : <Tile2DBack key={-index}/>);
    const ura_dora_tiles = info.scoring_info.ura_dora_tiles.map((tile, index) => tile ? <Tile2D tile={tile} key={tile}/> : <Tile2DBack key={-index}/>);
    winInfoInner = (
      <>
        <img
          class="avatar"
          src={winnerAvatar.imageURL}
          alt={winnerAvatar.name}
        />
        { dora_tiles.length > 0 ? (
          <div class="win_dora">
            <div class="dora_tiles">
              <span class="dora_label">Dora</span>
              {dora_tiles}
            </div>
            <div class="dora_tiles">
              <span class="dora_label">Ura</span>
              {ura_dora_tiles}
            </div>
          </div>
          ) : (<></>) }
        <div id="patterns">
          {Object.entries(info.scoring_info.patterns).map(([pattern, data]) => (
            <PatternInfo key={pattern} data={data} />
          ))}
        </div>
      </>
    );
  }
  return (
    <div id="win_info">
      <WinHand win_info={info.win_info} />
      {winInfoInner}
      <WinTotalScore
        win_player_name={
          info.scoring_info
            ? players[info.scoring_info.win_player].display_name
            : ""
        }
        scoring_info={info.scoring_info}
        goToResults={goToResults}
      />
    </div>
  );
}
