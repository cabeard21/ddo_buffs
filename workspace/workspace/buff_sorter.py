class BuffSorter:
    def sort(self, bars):
        return sorted(bars.items(), key=lambda x: x[1].size[0])
