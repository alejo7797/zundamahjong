export type Player = {
  display_name: string;
  id: string;
};

export type UserPlayer = Player & {
  has_account: boolean;
  new_user: boolean;
};
