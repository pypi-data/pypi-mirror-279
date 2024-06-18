"""Configuration module for BACore."""
import os
from bacore.domain import settings

docker_build = os.getenv("DOCKER_BUILD", None)

project_bacore = settings.Project(name="BACore",
                                  version="0.0.10",
                                  description="BACore is a framework for business analysis and test automation.")
