#Dynamic Storage Allocation







# Example usage

# Allocate blocks


# Deallocate block 2


if __name__ == '__main__':
    class MemoryBlock:
        def __init__(self, start_address, size):
            self.start_address = start_address
            self.size = size
            self.allocated = False
    class MemoryManager:
        def __init__(self, total_memory):
            self.total_memory = total_memory
            self.memory_blocks = [MemoryBlock(0, total_memory)]
        def allocate(self, size):
            for block in self.memory_blocks:
                if not block.allocated and block.size >= size:
                    block.allocated = True
                    return block.start_address
            return -1
        def deallocate(self, address):
            for block in self.memory_blocks:
                if block.start_address == address:
                    block.allocated = False
                    return
        def print_memory_map(self):
            print("Memory Map:")
            for block in self.memory_blocks:
                print(f"Address: {block.start_address} - Size: {block.size} - Allocated: {block.allocated}")
    manager = MemoryManager(100)
    block1_address = manager.allocate(20)
    block2_address = manager.allocate(30)
    block3_address = manager.allocate(10)
    manager.print_memory_map()
    manager.deallocate(block2_address)
    manager.print_memory_map()
