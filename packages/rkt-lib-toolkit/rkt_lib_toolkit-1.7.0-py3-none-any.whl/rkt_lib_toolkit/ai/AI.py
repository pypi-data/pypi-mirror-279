from typing import List, Optional

import numpy as np
import pandas as pd
from pandas import DataFrame

from rkt_lib_toolkit.config import Config
from rkt_lib_toolkit.logger import Logger


class QLearning:
    def __init__(self, actions: List, should_load: bool = False, qtable_file_to_load: str = "", alpha: float = 0.1,
                 gamma: float = 0.8, learning_method: str = "sarsa",
                 e_greedy: float = 0.5):

        self._me = self.__class__.__name__
        self._logger: Logger = Logger(caller_class=self.me)
        self._logger.set_logger(caller_class=self.me, output="stream")
        self._config: Config = Config()

        self.learning_rate: float = alpha
        self.discount_factor: float = gamma
        self.e_greedy = e_greedy

        self.qtable: Optional['DataFrame'] = None
        self.available_actions: list = actions
        self.previous_state: str = "start"
        self.previous_action: str = "do-nothing"

        self._learning_method = learning_method
        self._learning_methods = {}
        self._fill_up_lms()

        self.load(should_load, qtable_file_to_load)

    # PROPERTIES
    @property
    def me(self) -> str:
        return self._me

    @me.setter
    def me(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("The '_me' property must be a string")
        self._me: str = value

    @property
    def logger(self) -> Logger:
        return self._logger

    @logger.setter
    def logger(self, value: Logger) -> None:
        if not isinstance(value, Logger):
            raise TypeError("The '_logger' property must be a 'Logger'")
        self._logger: Logger = value

    @property
    def config(self) -> Config:
        return self._config

    @config.setter
    def config(self, value: Config) -> None:
        if not isinstance(value, Config):
            raise TypeError("The '_config' property must be a 'Config'")
        self._config: Config = value

    @property
    def learning_rate(self) -> float:
        return self._learning_rate

    @learning_rate.setter
    def learning_rate(self, value: float) -> None:
        if not isinstance(value, float):
            raise TypeError("The '_learning_rate' property must be a float")
        self._learning_rate: float = value

    @property
    def discount_factor(self) -> float:
        return self._discount_factor

    @discount_factor.setter
    def discount_factor(self, value: float) -> None:
        if not isinstance(value, float):
            raise TypeError("The '_discount_factor' property must be a float")
        self._discount_factor: float = value

    @property
    def qtable(self) -> 'DataFrame':
        return self._qtable

    @qtable.setter
    def qtable(self, value: 'DataFrame') -> None:
        if not isinstance(value, DataFrame) and value is not None:
            raise TypeError("The '_qtable' property must be a DataFrame")
        self._qtable: Optional['DataFrame'] = value

    @property
    def previous_state(self) -> str:
        return self._previous_state

    @previous_state.setter
    def previous_state(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("The '_previous_state' property must be a string")
        self._previous_state: str = value

    @property
    def previous_action(self) -> str:
        return self._previous_action

    @previous_action.setter
    def previous_action(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("The '_previous_action' property must be a string")
        self._previous_action: str = value

    @property
    def available_actions(self) -> List:
        return self._available_actions

    @available_actions.setter
    def available_actions(self, value: List) -> None:
        if not isinstance(value, List):
            raise TypeError("The '_available_actions' property must be a list")
        self._available_actions: List = value

    def __repr__(self) -> str:
        return f"QLearning(learning_rate={self.learning_rate}, discount_factor={self.discount_factor}, learning_method={self._learning_method})"

    # Functions
    # # Management
    def save(self, file: str) -> None:
        self.qtable.to_pickle(path=file, compression='gzip')
        print(f'Q-table is saved at {file}')

    def load(self, do_load: bool, file_to_load: str) -> None:
        if do_load:
            print(f'Loading Q-table from {file_to_load}')
            self.qtable = pd.read_pickle(filepath_or_buffer=file_to_load, compression='gzip')
        else:
            print("Create new DataFrame Qtable")
            self.qtable = pd.DataFrame(columns=self.available_actions, dtype=np.float64)

    # # Private
    def _fill_up_lms(self):
        self._learning_methods = {"sarsa": self._sarsa,
                                  "temporal_difference": self._temporal_difference,
                                  }

    def _sarsa(self, state: str, action: str, reward: float):
        if self.previous_state != "start":
            if len(self.qtable.index.tolist()) == 2:
                self.previous_state = "start"

            last_qvalue = float(self.qtable.loc[self.previous_state, self.previous_action])
            new_qvalue = float(reward + self.discount_factor * self.qtable.loc[state, action])

            self.qtable.loc[state, action] += self.learning_rate * (new_qvalue - last_qvalue)

    def _temporal_difference(self, state: str, action: str, reward: float):

        best_qvalue = float(np.argmax(self.qtable.loc[state, :]))
        prev2now_qvalue = float(self.qtable.loc[self.previous_state, action])

        self.qtable.loc[self.previous_state, action] += self.learning_rate * \
                                                        (reward + self.discount_factor * best_qvalue - prev2now_qvalue)

    # # AI
    def choose_action(self, state: str, available_actions: Optional[list] = None):
        available_actions = available_actions if available_actions else self.available_actions
        if self.previous_state == "start":
            e_greedy = 2
            state = self.previous_state
        else:
            e_greedy = self.e_greedy

        if np.random.uniform() < e_greedy:
            action = np.argmax(self.qtable.loc[state, :])
        else:
            action = np.random.choice([i for i in range(len(available_actions))])

        return self.available_actions[action]

    def learn(self, state: str, action, reward: float) -> None:
        self.check_state_exist(state)
        self._learning_methods[self._learning_method](state, action, reward)

        self.previous_state = state
        self.previous_action = action

    def check_state_exist(self, state: str):
        if state not in self.qtable.index:
            series_value = 0
            series_name = state
            if self.previous_state == "start":
                series_name = self.previous_state
                series_value = 1

            self.qtable.loc[series_name] = pd.Series([series_value] * len(self.available_actions),
                                                     index=self.qtable.columns, name=state)
