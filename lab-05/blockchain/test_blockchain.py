from blockchain import Blockchain

# 1. Khởi tạo Blockchain
print("--- Khởi tạo Blockchain ---")
my_blockchain = Blockchain()

# 2. Thêm các giao dịch (Transactions)
print("Đang thêm các giao dịch...")
my_blockchain.add_transaction('Alice', 'Bob', 10)
my_blockchain.add_transaction('Bob', 'Charlie', 5)
my_blockchain.add_transaction('Charlie', 'Alice', 3)

# 3. Đào một khối mới (Mining a new block)
print("Đang đào khối mới (Mining)...")
previous_block = my_blockchain.get_previous_block()
previous_proof = previous_block.proof
new_proof = my_blockchain.proof_of_work(previous_proof)
previous_hash = previous_block.hash

# Thêm phần thưởng cho thợ đào (Miner)
my_blockchain.add_transaction('Genesis', 'Miner', 1)

# Tạo khối mới và thêm vào chuỗi
new_block = my_blockchain.create_block(new_proof, previous_hash)

# 4. Hiển thị thông tin chuỗi Blockchain
print("\n--- Danh sách các khối trong chuỗi ---")
for block in my_blockchain.chain:
    print(f"Block #{block.index}")
    print(f"Timestamp: {block.timestamp}")
    print(f"Transactions: {block.transactions}")
    print(f"Proof: {block.proof}")
    print(f"Previous Hash: {block.previous_hash}")
    print(f"Hash: {block.hash}")
    print("-" * 30)

# 5. Kiểm tra tính hợp lệ của Blockchain
is_valid = my_blockchain.is_chain_valid(my_blockchain.chain)
print(f"Is Blockchain Valid: {is_valid}")