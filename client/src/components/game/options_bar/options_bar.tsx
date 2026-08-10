import { useContext, useState } from "preact/hooks";

import { Emitter } from "../../emitter/emitter";
import { GameOptionsForm } from "../options_form/game_options_form/game_options_form";
import { ClientOptionsForm } from "../options_form/client_options_form/client_options_form";
import { OptionsContext } from "../../options_context/options_context";

import "./options_bar.css";

export function OptionsBar() {
  const [isOpen, setIsOpen] = useState(false);
  const [isClickedEndGame, setIsClickedEndGame] = useState(false);
  const emit = useContext(Emitter);
  const options = useContext(OptionsContext)!;

  const showHideOptions = (e: Event) => {
    e.preventDefault();
    setIsOpen(!isOpen);
    setIsClickedEndGame(false);
  };

  const confirmEndGame = (e: Event) => {
    e.preventDefault();
    setIsClickedEndGame(true);
  };
  const yesEndGame = (e: Event) => {
    e.preventDefault();
    emit("end_game");
  };
  const noEndGame = (e: Event) => {
    e.preventDefault();
    setIsClickedEndGame(false);
  };

  return (
    <div class={`options_bar ${isOpen ? "open" : "closed"}`}>
      <button type="button" class="open_close" onClick={showHideOptions}>
        {isOpen ? "Hide options" : "View options"}
      </button>
      <div class="sidebar">
        <div class="end_game">
          <button type="button" onClick={confirmEndGame}>
            End game
          </button>
          <div class={`confirm_end_game ${isClickedEndGame ? "" : "hidden"}`}>
            <div class="confirm_end_game_message">
              Are you sure you want to end the game?
            </div>
            <button type="button" onClick={yesEndGame}>
              Yes
            </button>
            <button type="button" onClick={noEndGame}>
              No
            </button>
          </div>
        </div>
        <div class="game_options_title">Client Options</div>
        <ClientOptionsForm
          clientOptions={options.client_options}
          setClientOptions={options.set_client_options}
        />
        <div class="game_options_title">Game Options</div>
        <GameOptionsForm
          gameOptions={options.game_options}
          isEditable={false}
          can_start={false}
        />
      </div>
    </div>
  );
}
