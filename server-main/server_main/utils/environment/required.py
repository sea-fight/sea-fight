import os


def required_env_many(*env_variables: str) -> list[str]:
    """Function for safely retrieving environment variables.

    :param env_variables: The names of the constants whose value you want to get.
    :return: A collection of values of the constants in .env.
        The order of return is the same as the order in which arguments are transmitted.
    :raises EnvironmentError: If constant name not found in .env file.
    """
    values: list[str] = []
    not_found_env_variables: list[str] = []

    for env_var_name in env_variables:
        if (value := os.getenv(env_var_name)) is None:
            not_found_env_variables.append(env_var_name)
            continue
        values.append(value)

    if not_found_env_variables:
        raise EnvironmentError(
            "Please set up .env file with following constants: "
            + " ".join(not_found_env_variables),
        )

    return values


def required_env(env_variable: str) -> str:
    return required_env_many(env_variable)[0]
