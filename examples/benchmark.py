# examples/benchmark_fast.py
"""
Fast Benchmark for Crypto-Journey
==================================
Reduced iterations for faster benchmarking.
"""

import time
import sys
import warnings
from pathlib import Path

warnings.filterwarnings('ignore')
sys.path.append(str(Path(__file__).parent.parent))

# Import versions
from src.try_1 import encrypt as encrypt_1, decrypt as decrypt_1
from src.try_5 import encrypt as encrypt_5, decrypt as decrypt_5
from src.try_10 import encrypt as encrypt_10, decrypt as decrypt_10
from src.try_15 import ASA_Crypt as ASA_15
from src.try_19 import ASA_Crypt as ASA_19
from src.try_21 import ASA_Crypt as ASA_21
from src.try_23 import ASA_Crypt as ASA_23
from src.try_26 import ASA_Crypt as ASA_26


class FastBenchmark:
    """Fast benchmark with reduced iterations."""
    
    def __init__(self, iterations: int = 50, warmup: int = 5):
        self.iterations = iterations
        self.warmup = warmup
        self.results = {}
    
    def time_function(self, func, *args, **kwargs) -> float:
        """Time a function with warmup."""
        # Warmup
        for _ in range(self.warmup):
            try:
                func(*args, **kwargs)
            except:
                pass
        
        # Timing
        start = time.perf_counter()
        for _ in range(self.iterations):
            func(*args, **kwargs)
        end = time.perf_counter()
        
        return (end - start) / self.iterations
    
    def benchmark_version_10_fast(self):
        """Benchmark try_10 with reduced PBKDF2 iterations."""
        # Patch PBKDF2 to use fewer iterations
        import hashlib
        original_pbkdf2 = hashlib.pbkdf2_hmac
        
        def fast_pbkdf2(hash_name, password, salt, iterations, dklen):
            # Use only 1000 iterations for benchmarking
            return original_pbkdf2(hash_name, password, salt, 1000, dklen)
        
        hashlib.pbkdf2_hmac = fast_pbkdf2
        
        try:
            data = "Hello World! This is a test."
            key = "test-key"
            
            def encrypt_decrypt():
                encrypted = encrypt_10(data, key)
                return decrypt_10(encrypted, key)
            
            avg_time = self.time_function(encrypt_decrypt)
            self.results['try_10'] = {
                'time': avg_time,
                'description': 'Header + HMAC (fast)',
                'security': '🟡 LOW'
            }
        finally:
            # Restore original PBKDF2
            hashlib.pbkdf2_hmac = original_pbkdf2
    
    def benchmark_version_15_fast(self):
        """Benchmark try_15."""
        data = "Hello World! This is a test."
        key = "amirsam"
        crypt = ASA_15(key)
        
        def encrypt_decrypt():
            encrypted = crypt.encrypt(data)
            return crypt.decrypt(encrypted)
        
        avg_time = self.time_function(encrypt_decrypt)
        self.results['try_15'] = {
            'time': avg_time,
            'description': 'HKDF + Blake2s',
            'security': '🟡 MEDIUM'
        }
    
    def benchmark_version_19(self):
        """Benchmark try_19."""
        data = "Hello World! This is a test."
        key = b"test-key"
        crypt = ASA_19(key)
        
        def encrypt_decrypt():
            encrypted = crypt.encrypt(data)
            return crypt.decrypt(encrypted)
        
        avg_time = self.time_function(encrypt_decrypt)
        self.results['try_19'] = {
            'time': avg_time,
            'description': 'Set-based Replay',
            'security': '🟡 MEDIUM'
        }
    
    def benchmark_version_21(self):
        """Benchmark try_21."""
        data = "Hello World! This is a test."
        key = b"test-key"
        crypt = ASA_21(key)
        
        def encrypt_decrypt():
            encrypted = crypt.encrypt(data)
            return crypt.decrypt(encrypted)
        
        avg_time = self.time_function(encrypt_decrypt)
        self.results['try_21'] = {
            'time': avg_time,
            'description': 'Bitmap-based Replay',
            'security': '🟡 MEDIUM-HIGH'
        }
    
    def benchmark_version_23(self):
        """Benchmark try_23."""
        data = "Hello World! This is a test."
        key = b"test-key"
        crypt = ASA_23(key)
        
        def encrypt_decrypt():
            encrypted = crypt.encrypt(data)
            return crypt.decrypt(encrypted)
        
        avg_time = self.time_function(encrypt_decrypt)
        self.results['try_23'] = {
            'time': avg_time,
            'description': 'Auto-Reset Bitmap',
            'security': '🟢 MEDIUM-HIGH'
        }
    
    def benchmark_version_26(self):
        """Benchmark try_26."""
        data = "Hello World! This is a test."
        key = b"test-key"
        crypt = ASA_26(key)
        
        def encrypt_decrypt():
            encrypted = crypt.encrypt(data)
            return crypt.decrypt(encrypted)
        
        avg_time = self.time_function(encrypt_decrypt)
        self.results['try_26'] = {
            'time': avg_time,
            'description': 'Cuckoo Filter + Blake2b',
            'security': '🟢 HIGH'
        }
    
    def run(self):
        """Run all benchmarks."""
        print("⚡ FAST BENCHMARK (Reduced iterations)")
        print("="*70)
        print(f"📊 {self.iterations} iterations per version")
        print(f"🔥 {self.warmup} warmup iterations")
        print("="*70)
        
        # Fast versions first
        versions = [
            ('try_1', self.benchmark_version_1),
            ('try_5', self.benchmark_version_5),
            ('try_10_fast', self.benchmark_version_10_fast),
            ('try_15', self.benchmark_version_15_fast),
            ('try_19', self.benchmark_version_19),
            ('try_21', self.benchmark_version_21),
            ('try_23', self.benchmark_version_23),
            ('try_26', self.benchmark_version_26),
        ]
        
        for name, func in versions:
            print(f"⏳ Benchmarking {name}...", end='', flush=True)
            try:
                func()
                print(" ✅")
            except Exception as e:
                print(f" ❌ {e}")
        
        self.display_results()
    
    def benchmark_version_1(self):
        """Benchmark try_1."""
        data = "Hello World! This is a test."
        key = "test-key"
        
        def encrypt_decrypt():
            encrypted = encrypt_1(data, key)
            return decrypt_1(encrypted, key)
        
        avg_time = self.time_function(encrypt_decrypt)
        self.results['try_1'] = {
            'time': avg_time,
            'description': 'Basic Sum Encryption',
            'security': '🔴 VERY LOW'
        }
    
    def benchmark_version_5(self):
        """Benchmark try_5."""
        data = "Hello World! This is a test."
        key = "test-key"
        
        def encrypt_decrypt():
            encrypted = encrypt_5(data, key)
            return decrypt_5(encrypted, key)
        
        avg_time = self.time_function(encrypt_decrypt)
        self.results['try_5'] = {
            'time': avg_time,
            'description': 'Optimized XOR + Hex',
            'security': '🔴 VERY LOW'
        }
    
    def display_results(self):
        """Display benchmark results."""
        print("\n📈 RESULTS:")
        print("="*70)
        print(f"{'Version':<12} {'Time (ms)':<15} {'Security':<12} {'Description'}")
        print("-"*70)
        
        if not self.results:
            print("❌ No results")
            return
        
        sorted_results = sorted(self.results.items(), key=lambda x: x[1]['time'])
        fastest_time = sorted_results[0][1]['time']
        
        for version, data in sorted_results:
            time_ms = data['time'] * 1000
            speed = f"{time_ms:.3f}ms"
            
            if data['time'] == fastest_time:
                relative = "🚀 fastest"
            else:
                ratio = data['time'] / fastest_time
                relative = f"{ratio:.1f}x"
            
            print(f"{version:<12} {speed:<15} {data['security']:<12} {data['description']}")
            print(f"             ({relative})")
        
        print("-"*70)
        
        print("\n📊 SUMMARY:")
        print(f"🔹 Fastest: {sorted_results[0][0]} ({sorted_results[0][1]['description']})")
        print(f"🔹 Slowest: {sorted_results[-1][0]} ({sorted_results[-1][1]['description']})")


def main():
    """Run fast benchmark."""
    try:
        benchmark = FastBenchmark(iterations=50, warmup=5)
        benchmark.run()
    except KeyboardInterrupt:
        print("\n\n⏹️ Interrupted")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()