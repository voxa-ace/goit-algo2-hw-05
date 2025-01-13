import hashlib

class BloomFilter:
    """
    A Bloom Filter implementation for checking the existence of items
    without storing them explicitly.
    """
    def __init__(self, size=1000, num_hashes=3):
        """
        :param size: The size of the internal bit array.
        :param num_hashes: The number of hash functions to use.
        """
        self.size = size
        self.num_hashes = num_hashes
        # We represent our bit array as a list of booleans
        self.bits = [False] * size

    def _hashes(self, item):
        """
        Generates multiple hash values for a single item.
        We can use different algorithms like MD5, SHA1, or SHA256.
        Here, we append a salt (index i) to the item for each hash.
        """
        results = []
        for i in range(self.num_hashes):
            salted_value = f"{item}-{i}".encode('utf-8')
            # Using SHA256 as an example
            hash_digest = hashlib.sha256(salted_value).hexdigest()
            # Convert the hex digest to an integer and take modulo 'self.size'
            position = int(hash_digest, 16) % self.size
            results.append(position)
        return results

    def add(self, item):
        """
        Adds an item to the Bloom filter by setting the corresponding
        positions in the bit array to True.
        """
        for pos in self._hashes(item):
            self.bits[pos] = True

    def contains(self, item):
        """
        Checks if an item might be in the filter.
        If at least one of the corresponding positions is False,
        the item is definitely not in the filter.
        """
        for pos in self._hashes(item):
            if not self.bits[pos]:
                return False
        return True


def check_password_uniqueness(bloom_filter, new_passwords):
    """
    Checks a list of new passwords against the Bloom filter.
    Returns a dictionary with the status of each password:
      - "already used" if it might exist in the filter
      - "unique" if it wasn't previously added and is now added to the filter
      - "invalid password" if the password is empty or not a string
    """
    results = {}
    for pwd in new_passwords:
        # Handle cases where password is None or empty
        if not isinstance(pwd, str) or pwd.strip() == "":
            results[pwd] = "invalid password"
            continue

        if bloom_filter.contains(pwd):
            results[pwd] = "already used"
        else:
            bloom_filter.add(pwd)
            results[pwd] = "unique"
    return results


if __name__ == "__main__":
    # 1. Initialize the Bloom filter
    bloom = BloomFilter(size=1000, num_hashes=3)

    # 2. Add existing passwords
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for p in existing_passwords:
        bloom.add(p)

    # 3. Check new passwords
    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest", "", None]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    # 4. Print results
    for password, status in results.items():
        print(f"Password '{password}' - {status}.")
