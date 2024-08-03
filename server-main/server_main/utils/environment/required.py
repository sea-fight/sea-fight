import os


def required_env_many(*env_variables: str) -> list[str]:
    """
    Retrieve multiple environment variables safely.

    Args:
        env_variables (str): Names of the environment variables to retrieve.

    Returns:
        list[str]: Values of the requested environment variables in the same order as the arguments.

    Raises:
        EnvironmentError: If any of the specified environment variables are not found.
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
            "Please set up .env file with the following constants: "
            + " ".join(not_found_env_variables),
        )

    return values


def required_env(env_variable: str) -> str:
    """
    Retrieve a single environment variable safely.

    Args:
        env_variable (str): Name of the environment variable to retrieve.

    Returns:
        str: Value of the requested environment variable.

    Raises:
        EnvironmentError: If the specified environment variable is not found.
    """
    return required_env_many(env_variable)[0]
