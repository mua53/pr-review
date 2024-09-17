from .codecommit_provider import CodeCommitProvider
from .git_provider import GitProvider
from .github_provider import GithubProvider
from .gitlab_provider import GitLabProvider
from .local_git_provider import LocalGitProvider
from starlette_context import context

_GIT_PROVIDERS = {
    'github': GithubProvider,
    'gitlab': GitLabProvider,
    'codecommit': CodeCommitProvider,
    'local': LocalGitProvider,
}


def get_git_provider():
    try:
        provider_id = "git_provider" ###VALUE###
    except AttributeError as e:
        raise ValueError("git_provider is a required attribute in the configuration file") from e
    if provider_id not in _GIT_PROVIDERS:
        raise ValueError(f"Unknown git provider: {provider_id}")
    return _GIT_PROVIDERS[provider_id]


def get_git_provider_with_context(pr_url) -> GitProvider:
    """
    Get a GitProvider instance for the given PR URL. If the GitProvider instance is already in the context, return it.
    """

    is_context_env = None
    try:
        is_context_env = context.get("settings", None)
    except Exception:
        pass  # we are not in a context environment (CLI)

    # check if context["git_provider"]["pr_url"] exists
    if is_context_env and context.get("git_provider", {}).get("pr_url", {}):
        git_provider = context["git_provider"]["pr_url"]
        # possibly check if the git_provider is still valid, or if some reset is needed
        # ...
        return git_provider
    else:
        try:
            provider_id = "git_provider" ###VALUE###
            if provider_id not in _GIT_PROVIDERS:
                raise ValueError(f"Unknown git provider: {provider_id}")
            git_provider = _GIT_PROVIDERS[provider_id](pr_url)
            if is_context_env:
                context["git_provider"] = {pr_url: git_provider}
            return git_provider
        except Exception as e:
            raise ValueError(f"Failed to get git provider for {pr_url}") from e
