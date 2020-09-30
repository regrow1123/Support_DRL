from datetime import datetime

from stable_baselines3 import PPO
from stable_baselines3.common.cmd_util import make_vec_env
from stable_baselines3.common.callbacks import CheckpointCallback

from env import SupportEnv, LegalActionWrapper, ROIWrapper, ImageToPyTorch, ScaledFloatFrame
from policy import MyActorCriticPolicy
from model import ResFeatureExtractor


def linear_schedule(initial_value, final_value):
    """
    Linear learning rate schedule.
    :param initial_value: (float or str)
    :return: (function)
    """
    def func(progress):
        """
        Progress will decrease from 1 (beginning) to 0
        :param progress: (float)
        :return: (float)
        """
        return progress * (initial_value-final_value) + final_value

    return func


if __name__ == "__main__":
    seed = 0
    n_envs = 8
    wrapper_class = lambda env: ScaledFloatFrame(
        ImageToPyTorch(LegalActionWrapper(ROIWrapper(env)))
    )
<<<<<<< HEAD
    env_kwargs = dict(board_size=50, zoffset=10, reward=0.05, penalty=0.005)
    features_extractor_kwargs = dict(n_channel=128, n_block=12)
    optimizer_kwargs = dict(weight_decay=1e-4)
=======
    env_kwargs = dict(board_size=30, zoffset=8, reward=0.1, penalty=0.001)
    features_extractor_kwargs = dict(n_channel=128, n_block=8)
    optimizer_kwargs = dict(weight_decay=0)
>>>>>>> 6e1306cdf173ec9e166a3301c9388c27fe35483c
    ppo_kwargs = dict(
        learning_rate=linear_schedule(2.5e-4, 0.5e-4),
        n_steps=256,
        batch_size=64,
        n_epochs=10,
<<<<<<< HEAD
        gamma=0.9,
=======
        gamma=0.95,
>>>>>>> 6e1306cdf173ec9e166a3301c9388c27fe35483c
        gae_lambda=0.95,
        clip_range=0.2,
        clip_range_vf=0.2,
        ent_coef=0.01,
        vf_coef=0.5,
        max_grad_norm=0.5,
        target_kl=0.05,
        verbose=1,
        seed=seed
    )
    policy_kwargs = dict(
        valuehead_hidden=512,
        features_extractor_class=ResFeatureExtractor,
        features_extractor_kwargs=features_extractor_kwargs,
        optimizer_kwargs=optimizer_kwargs,
    )

    env = make_vec_env(
        SupportEnv,
        n_envs,
        seed=seed,
        wrapper_class=wrapper_class,
        env_kwargs=env_kwargs,
    )

    now = datetime.now()
    date_time = now.strftime("%m.%d.%Y_%Hh%Mm%Ss")
    model = PPO(
        MyActorCriticPolicy,
        env,
        **ppo_kwargs,
        tensorboard_log=f"runs/{date_time}",
        policy_kwargs=policy_kwargs,
    )
    print(model.policy)
    model.save("./logs/rl_model_0_steps")

    checkpoint_callback = CheckpointCallback(
        save_freq=int(2e5), save_path="./logs/", name_prefix="rl_model"
    )
    model.learn(
        total_timesteps=int(1e7),
        reset_num_timesteps=False,
        callback=checkpoint_callback,
    )
    model.save("./logs/rl_model_last")
