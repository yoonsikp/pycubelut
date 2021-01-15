ERROR: All suitable heaps are exhausted. Heaps {
    types: [
        MemoryType {
            heap_index: 0,
            properties: DEVICE_LOCAL,
            dedicated: DedicatedAllocator {
                memory_type: MemoryTypeId(
                    0,
                ),
                memory_properties: DEVICE_LOCAL,
                non_coherent_atom_size: None,
                used: 0,
            },
            general: GeneralAllocator {
                memory_type: MemoryTypeId(
                    0,
                ),
                memory_properties: DEVICE_LOCAL,
                block_size_granularity: 256,
                max_chunk_size: 16777216,
                min_device_allocation: 65536,
                sizes: {},
                chunks: {},
                non_coherent_atom_size: None,
            },
            linear: LinearAllocator {
                memory_type: MemoryTypeId(
                    0,
                ),
                memory_properties: DEVICE_LOCAL,
                linear_size: 16777216,
                offset: 0,
                lines: [],
                non_coherent_atom_size: None,
            },
            used: 0,
            effective: 0,
        },
        MemoryType {
            heap_index: 1,
            properties: CPU_VISIBLE | COHERENT,
            dedicated: DedicatedAllocator {
                memory_type: MemoryTypeId(
                    1,
                ),
                memory_properties: CPU_VISIBLE | COHERENT,
                non_coherent_atom_size: None,
                used: 0,
            },
            general: GeneralAllocator {
                memory_type: MemoryTypeId(
                    1,
                ),
                memory_properties: CPU_VISIBLE | COHERENT,
                block_size_granularity: 256,
                max_chunk_size: 16777216,
                min_device_allocation: 65536,
                sizes: {},
                chunks: {},
                non_coherent_atom_size: None,
            },
            linear: LinearAllocator {
                memory_type: MemoryTypeId(
                    1,
                ),
                memory_properties: CPU_VISIBLE | COHERENT,
                linear_size: 16777216,
                offset: 0,
                lines: [],
                non_coherent_atom_size: None,
            },
            used: 0,
            effective: 0,
        },
        MemoryType {
            heap_index: 1,
            properties: DEVICE_LOCAL | CPU_VISIBLE,
            dedicated: DedicatedAllocator {
                memory_type: MemoryTypeId(
                    2,
                ),
                memory_properties: DEVICE_LOCAL | CPU_VISIBLE,
                non_coherent_atom_size: Some(
                    4,
                ),
                used: 0,
            },
            general: GeneralAllocator {
                memory_type: MemoryTypeId(
                    2,
                ),
                memory_properties: DEVICE_LOCAL | CPU_VISIBLE,
                block_size_granularity: 256,
                max_chunk_size: 16777216,
                min_device_allocation: 65536,
                sizes: {
                    144000000: SizeEntry {
                        total_blocks: 4,
                        ready_chunks: BitSet {
                            layer3: 1,
                            layer2: [
                                1,
                            ],
                            layer1: [
                                1,
                            ],
                            layer0: [
                                6,
                            ],
                        },
                        chunks: Slab { len: 3, cap: 4 },
                    },
                    187648: SizeEntry {
                        total_blocks: 1,
                        ready_chunks: BitSet {
                            layer3: 0,
                            layer2: [],
                            layer1: [],
                            layer0: [],
                        },
                        chunks: Slab { len: 1, cap: 1 },
                    },
                    256: SizeEntry {
                        total_blocks: 2,
                        ready_chunks: BitSet {
                            layer3: 1,
                            layer2: [
                                1,
                            ],
                            layer1: [
                                1,
                            ],
                            layer0: [
                                1,
                            ],
                        },
                        chunks: Slab { len: 1, cap: 1 },
                    },
                    2048: SizeEntry {
                        total_blocks: 1,
                        ready_chunks: BitSet {
                            layer3: 1,
                            layer2: [
                                1,
                            ],
                            layer1: [
                                1,
                            ],
                            layer0: [
                                1,
                            ],
                        },
                        chunks: Slab { len: 1, cap: 1 },
                    },
                    16384: SizeEntry {
                        total_blocks: 1,
                        ready_chunks: BitSet {
                            layer3: 1,
                            layer2: [
                                1,
                            ],
                            layer1: [
                                1,
                            ],
                            layer0: [
                                1,
                            ],
                        },
                        chunks: Slab { len: 1, cap: 1 },
                    },
                    131072: SizeEntry {
                        total_blocks: 1,
                        ready_chunks: BitSet {
                            layer3: 0,
                            layer2: [],
                            layer1: [],
                            layer0: [],
                        },
                        chunks: Slab { len: 1, cap: 1 },
                    },
                    431360: SizeEntry {
                        total_blocks: 1,
                        ready_chunks: BitSet {
                            layer3: 0,
                            layer2: [],
                            layer1: [],
                            layer0: [],
                        },
                        chunks: Slab { len: 1, cap: 1 },
                    },
                },
                chunks: {},
                non_coherent_atom_size: Some(
                    4,
                ),
            },
            linear: LinearAllocator {
                memory_type: MemoryTypeId(
                    2,
                ),
                memory_properties: DEVICE_LOCAL | CPU_VISIBLE,
                linear_size: 16777216,
                offset: 0,
                lines: [],
                non_coherent_atom_size: Some(
                    4,
                ),
            },
            used: 1008750080,
            effective: 576619520,
        },
        MemoryType {
            heap_index: 1,
            properties: DEVICE_LOCAL | CPU_VISIBLE | CPU_CACHED,
            dedicated: DedicatedAllocator {
                memory_type: MemoryTypeId(
                    3,
                ),
                memory_properties: DEVICE_LOCAL | CPU_VISIBLE | CPU_CACHED,
                non_coherent_atom_size: Some(
                    4,
                ),
                used: 0,
            },
            general: GeneralAllocator {
                memory_type: MemoryTypeId(
                    3,
                ),
                memory_properties: DEVICE_LOCAL | CPU_VISIBLE | CPU_CACHED,
                block_size_granularity: 256,
                max_chunk_size: 16777216,
                min_device_allocation: 65536,
                sizes: {},
                chunks: {},
                non_coherent_atom_size: Some(
                    4,
                ),
            },
            linear: LinearAllocator {
                memory_type: MemoryTypeId(
                    3,
                ),
                memory_properties: DEVICE_LOCAL | CPU_VISIBLE | CPU_CACHED,
                linear_size: 16777216,
                offset: 0,
                lines: [],
                non_coherent_atom_size: Some(
                    4,
                ),
            },
            used: 0,
            effective: 0,
        },
    ],
    heaps: [
        MemoryHeap {
            size: 18446744073709551615,
            used: 0,
            effective: 0,
        },
        MemoryHeap {
            size: 1073741824,
            used: 1008750080,
            effective: 576619520,
        },
    ],
}
thread '<unnamed>' panicked at 'called `Result::unwrap()` on an `Err` value: AllocationError(OutOfMemory(Device))', /Users/runner/.cargo/git/checkouts/wgpu-53e70f8674b08dd4/6650b94/wgpu-core/src/device/mod.rs:358:22
