import { useContext } from "preact/hooks";

import type { Player } from "../../../types/player";
import { avatars, type AvatarIdDict } from "../../../types/avatars";

import { Emitter } from "../../emitter/emitter";

import "./avatar_selector.css";

export function AvatarSelector({
  player,
  canEdit,
  canKick,
  avatarId,
}: {
  player: Player;
  canEdit: boolean;
  canKick: boolean;
  avatarId: number;
}) {
  const emit = useContext(Emitter);
  const avatar = avatars[avatarId];
  const kickFromRoom = (e: Event) => {
    e.preventDefault();
    emit("kick_from_room", player.id);
  };
  const increaseAvatarId = (e: Event) => {
    e.preventDefault();
    emit("set_avatar", player.id, (avatarId + 1) % avatars.length);
  };
  const decreaseAvatarId = (e: Event) => {
    e.preventDefault();
    emit(
      "set_avatar",
      player.id,
      (avatarId + avatars.length - 1) % avatars.length,
    );
  };
  return (
    <div class="avatar_selector">
      <div class="avatar_selector_image_div">
        <img
          class="avatar_selector_image"
          src={avatar.imageURL}
          alt={avatar.name}
        />
        {canKick ? (
          <button type="button" class="kick_from_room" onClick={kickFromRoom}>
            &times;
          </button>
        ) : (
          <></>
        )}
      </div>
      <div class="avatar_selector_player_name">{player.display_name}</div>
      {canEdit ? (
        <>
          <button
            type="button"
            class="avatar_selector_decrease"
            onClick={decreaseAvatarId}
          >
            Prev
          </button>
          <button
            type="button"
            class="avatar_selector_increase"
            onClick={increaseAvatarId}
          >
            Next
          </button>
        </>
      ) : (
        <></>
      )}
    </div>
  );
}

export function AvatarDisplay({
  myPlayer,
  players,
  avatars,
}: {
  myPlayer: Player;
  players: ReadonlyArray<Player>;
  avatars: AvatarIdDict;
}) {
  const isCaptain =
    players.filter((player) => !player.id.startsWith("bot:"))[0].id ==
    myPlayer.id;
  return (
    <div class="avatar_display">
      {players.map((player) => (
        <AvatarSelector
          key={player.id}
          player={player}
          canEdit={
            player.id == myPlayer.id ||
            (player.id.startsWith("bot:") && isCaptain)
          }
          canKick={player.id != myPlayer.id && isCaptain}
          avatarId={avatars[player.id]}
        />
      ))}
    </div>
  );
}
