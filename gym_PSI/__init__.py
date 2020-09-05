from gym.envs.registration import register
try:
    register(
        id='CartPole-v2',
        entry_point='gym_PSI.envs:CartPoleEnv',
        )
except :
    pass