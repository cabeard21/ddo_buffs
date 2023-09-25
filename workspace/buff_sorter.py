import logging
import os


class BuffSorter:

    def __init__(self, buff_order, stack_buffs):
        self.buff_order = buff_order
        self.stack_buffs = stack_buffs
        self.logger = self._setup_logger()

        self.order_dict = self.create_order_dict()

    def _setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(
            os.path.join(os.path.dirname(os.path.realpath(__file__)),
                         'buff_sorter.log'))
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def create_order_dict(self):
        order_dict = {}
        for index, buff in enumerate(self.buff_order):
            if buff in self.stack_buffs:
                for stack_buff in self.stack_buffs[buff]:
                    order_dict[stack_buff] = index
                    self.logger.debug(
                        f'Assigned order {index} to stack buff {stack_buff}')
            else:
                order_dict[buff] = index
                self.logger.debug(f'Assigned order {index} to buff {buff}')
        return order_dict

    def sort(self, bars):
        sorted_bars = sorted(
            bars.items(),
            key=lambda x: self.order_dict.get(x[0], float('inf')))
        self.logger.debug(
            f'Sorted bars order: {[buff[0] for buff in sorted_bars]}')
        return sorted_bars
