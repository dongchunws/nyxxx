from tqdm import tqdm


class TqdmUploadWrapper:
    """File-like wrapper that updates tqdm progress bar on read()"""
    
    def __init__(self, file_obj, total_size, description):
        self._file_obj = file_obj
        self.total_size = total_size
        self._pbar = tqdm(
            total=total_size,
            unit='B',
            unit_scale=True,
            desc=description,
            ascii=True
        )

    def read(self, size=-1):
        chunk = self._file_obj.read(size)
        if chunk:
            self._pbar.update(len(chunk))
        else:
            if self._pbar.n < self.total_size:
                self._pbar.update(self.total_size - self._pbar.n)
            self._pbar.close()
        return chunk
    
    def __len__(self):
        return self.total_size
