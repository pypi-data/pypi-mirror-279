from abc import ABC
from datetime import timedelta
from typing import Optional

from tecton._internals.display import Displayable
from tecton.framework.dataset import SavedDataset


class TectonJob(ABC):
    def cancel_job(self) -> bool:
        pass

    # wait for all sub-tasks to complete
    def wait_for_completion(self, timeout: Optional[timedelta] = None):
        pass

    def get_job_status_for_display(self) -> Displayable:
        pass


class DatasetJob(TectonJob):
    _dataset: SavedDataset

    # cancel all sub-tasks
    def cancel_job(self) -> bool:
        pass

    # wait for all sub-tasks to complete
    def wait_for_completion(self, timeout: Optional[timedelta] = None):
        pass

    # return dataset object, if job is completed
    def get_dataset(self) -> Optional[SavedDataset]:
        return self._dataset

    def get_job_status_for_display(self) -> Displayable:
        pass
