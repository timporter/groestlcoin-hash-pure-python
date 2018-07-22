from copy import deepcopy
from functools import reduce

class base_hash(object):
    def __init__(self, initial_pt = None):
        if initial_pt is not None:
            self.update(initial_pt)

    def hexdigest(self, pt = None):
        return self.digest(pt).encode('hex')
    
    def digest(self, pt = None):
        self.update(pt)
        finalisedResult = self.finalise()
        groestl_state.dump('Finalised result', finalisedResult)
        return finalisedResult

def xor(*args):
    assert len(args) > 0
    accum = list(args[0])

    for x in args[1:]:
        assert len(x) == len(accum)
        for i in range(len(accum)):
            accum[i] ^= x[i]

    return accum

assert xor((0x01, 0x02, 0x04), (0x41, 0x52, 0x64)) == [0x40, 0x50, 0x60]

aes_sbox = [
  0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5,
  0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
  0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0,
  0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
  0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc,
  0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
  0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a,
  0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
  0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0,
  0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
  0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b,
  0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
  0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85,
  0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
  0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5,
  0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
  0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17,
  0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
  0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88,
  0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
  0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c,
  0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
  0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9,
  0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
  0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6,
  0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
  0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e,
  0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
  0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94,
  0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
  0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68,
  0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16,
]

mixbytes_matrix = [
  [2, 2, 3, 4, 5, 3, 5, 7],
  [7, 2, 2, 3, 4, 5, 3, 5],
  [5, 7, 2, 2, 3, 4, 5, 3],
  [3, 5, 7, 2, 2, 3, 4, 5],
  [5, 3, 5, 7, 2, 2, 3, 4],
  [4, 5, 3, 5, 7, 2, 2, 3],
  [3, 4, 5, 3, 5, 7, 2, 2],
  [2, 3, 4, 5, 3, 5, 7, 2]
]

gf256_exp = [
  0x01, 0x03, 0x05, 0x0f, 0x11, 0x33, 0x55, 0xff,
  0x1a, 0x2e, 0x72, 0x96, 0xa1, 0xf8, 0x13, 0x35,
  0x5f, 0xe1, 0x38, 0x48, 0xd8, 0x73, 0x95, 0xa4,
  0xf7, 0x02, 0x06, 0x0a, 0x1e, 0x22, 0x66, 0xaa,
  0xe5, 0x34, 0x5c, 0xe4, 0x37, 0x59, 0xeb, 0x26,
  0x6a, 0xbe, 0xd9, 0x70, 0x90, 0xab, 0xe6, 0x31,
  0x53, 0xf5, 0x04, 0x0c, 0x14, 0x3c, 0x44, 0xcc,
  0x4f, 0xd1, 0x68, 0xb8, 0xd3, 0x6e, 0xb2, 0xcd,
  0x4c, 0xd4, 0x67, 0xa9, 0xe0, 0x3b, 0x4d, 0xd7,
  0x62, 0xa6, 0xf1, 0x08, 0x18, 0x28, 0x78, 0x88,
  0x83, 0x9e, 0xb9, 0xd0, 0x6b, 0xbd, 0xdc, 0x7f,
  0x81, 0x98, 0xb3, 0xce, 0x49, 0xdb, 0x76, 0x9a,
  0xb5, 0xc4, 0x57, 0xf9, 0x10, 0x30, 0x50, 0xf0,
  0x0b, 0x1d, 0x27, 0x69, 0xbb, 0xd6, 0x61, 0xa3,
  0xfe, 0x19, 0x2b, 0x7d, 0x87, 0x92, 0xad, 0xec,
  0x2f, 0x71, 0x93, 0xae, 0xe9, 0x20, 0x60, 0xa0,
  0xfb, 0x16, 0x3a, 0x4e, 0xd2, 0x6d, 0xb7, 0xc2,
  0x5d, 0xe7, 0x32, 0x56, 0xfa, 0x15, 0x3f, 0x41,
  0xc3, 0x5e, 0xe2, 0x3d, 0x47, 0xc9, 0x40, 0xc0,
  0x5b, 0xed, 0x2c, 0x74, 0x9c, 0xbf, 0xda, 0x75,
  0x9f, 0xba, 0xd5, 0x64, 0xac, 0xef, 0x2a, 0x7e,
  0x82, 0x9d, 0xbc, 0xdf, 0x7a, 0x8e, 0x89, 0x80,
  0x9b, 0xb6, 0xc1, 0x58, 0xe8, 0x23, 0x65, 0xaf,
  0xea, 0x25, 0x6f, 0xb1, 0xc8, 0x43, 0xc5, 0x54,
  0xfc, 0x1f, 0x21, 0x63, 0xa5, 0xf4, 0x07, 0x09,
  0x1b, 0x2d, 0x77, 0x99, 0xb0, 0xcb, 0x46, 0xca,
  0x45, 0xcf, 0x4a, 0xde, 0x79, 0x8b, 0x86, 0x91,
  0xa8, 0xe3, 0x3e, 0x42, 0xc6, 0x51, 0xf3, 0x0e,
  0x12, 0x36, 0x5a, 0xee, 0x29, 0x7b, 0x8d, 0x8c,
  0x8f, 0x8a, 0x85, 0x94, 0xa7, 0xf2, 0x0d, 0x17,
  0x39, 0x4b, 0xdd, 0x7c, 0x84, 0x97, 0xa2, 0xfd,
  0x1c, 0x24, 0x6c, 0xb4, 0xc7, 0x52, 0xf6, 0x01,
]

gf256_log = [
  0x00, 0x00, 0x19, 0x01, 0x32, 0x02, 0x1a, 0xc6,
  0x4b, 0xc7, 0x1b, 0x68, 0x33, 0xee, 0xdf, 0x03,
  0x64, 0x04, 0xe0, 0x0e, 0x34, 0x8d, 0x81, 0xef,
  0x4c, 0x71, 0x08, 0xc8, 0xf8, 0x69, 0x1c, 0xc1,
  0x7d, 0xc2, 0x1d, 0xb5, 0xf9, 0xb9, 0x27, 0x6a,
  0x4d, 0xe4, 0xa6, 0x72, 0x9a, 0xc9, 0x09, 0x78,
  0x65, 0x2f, 0x8a, 0x05, 0x21, 0x0f, 0xe1, 0x24,
  0x12, 0xf0, 0x82, 0x45, 0x35, 0x93, 0xda, 0x8e,
  0x96, 0x8f, 0xdb, 0xbd, 0x36, 0xd0, 0xce, 0x94,
  0x13, 0x5c, 0xd2, 0xf1, 0x40, 0x46, 0x83, 0x38,
  0x66, 0xdd, 0xfd, 0x30, 0xbf, 0x06, 0x8b, 0x62,
  0xb3, 0x25, 0xe2, 0x98, 0x22, 0x88, 0x91, 0x10,
  0x7e, 0x6e, 0x48, 0xc3, 0xa3, 0xb6, 0x1e, 0x42,
  0x3a, 0x6b, 0x28, 0x54, 0xfa, 0x85, 0x3d, 0xba,
  0x2b, 0x79, 0x0a, 0x15, 0x9b, 0x9f, 0x5e, 0xca,
  0x4e, 0xd4, 0xac, 0xe5, 0xf3, 0x73, 0xa7, 0x57,
  0xaf, 0x58, 0xa8, 0x50, 0xf4, 0xea, 0xd6, 0x74,
  0x4f, 0xae, 0xe9, 0xd5, 0xe7, 0xe6, 0xad, 0xe8,
  0x2c, 0xd7, 0x75, 0x7a, 0xeb, 0x16, 0x0b, 0xf5,
  0x59, 0xcb, 0x5f, 0xb0, 0x9c, 0xa9, 0x51, 0xa0,
  0x7f, 0x0c, 0xf6, 0x6f, 0x17, 0xc4, 0x49, 0xec,
  0xd8, 0x43, 0x1f, 0x2d, 0xa4, 0x76, 0x7b, 0xb7,
  0xcc, 0xbb, 0x3e, 0x5a, 0xfb, 0x60, 0xb1, 0x86,
  0x3b, 0x52, 0xa1, 0x6c, 0xaa, 0x55, 0x29, 0x9d,
  0x97, 0xb2, 0x87, 0x90, 0x61, 0xbe, 0xdc, 0xfc,
  0xbc, 0x95, 0xcf, 0xcd, 0x37, 0x3f, 0x5b, 0xd1,
  0x53, 0x39, 0x84, 0x3c, 0x41, 0xa2, 0x6d, 0x47,
  0x14, 0x2a, 0x9e, 0x5d, 0x56, 0xf2, 0xd3, 0xab,
  0x44, 0x11, 0x92, 0xd9, 0x23, 0x20, 0x2e, 0x89,
  0xb4, 0x7c, 0xb8, 0x26, 0x77, 0x99, 0xe3, 0xa5,
  0x67, 0x4a, 0xed, 0xde, 0xc5, 0x31, 0xfe, 0x18,
  0x0d, 0x63, 0x8c, 0x80, 0xc0, 0xf7, 0x70, 0x07,
]

class groestl_state(object):
    def __init__(self, sz):
        assert 8 <= sz <= 512
        assert sz % 8 == 0
        self.sz = sz
        self.szbytes = self.sz // 8
        self.clear()

    def clone(self):
        return deepcopy(self)

    def add(self, pt):
        self.mbytes += len(pt)
        self.window.extend(x if isinstance(x, int) else int.from_bytes(x, 'big') for x in pt)
        self.take()

    def take(self):
        while len(self.window) >= self.lbytes:
            m = self.window[:self.lbytes]
            self.window = self.window[self.lbytes:]
            self.compress(m)

    def finalise(self):
        lenbytes = 8
        pads = (- self.mbytes - lenbytes - 1) % self.lbytes
        total = self.mbytes + pads + 1 + lenbytes
        assert total % self.lbytes == 0
        blocks = total // self.lbytes
        self.add(b'\x80' + b'\x00' * pads + blocks.to_bytes(8, 'big'))

        assert len(self.window) == 0

        # output transform
        result = xor(self.P(self.state), self.state)
        return bytes(result)[-self.szbytes:]

    def compress(self, m):
        pr = self.P(xor(m, self.state))
        qr = self.Q(m)
        self.state = xor(self.state, qr, pr)

    @staticmethod
    def dump(why, v):
              
        print(why + ': ')
        buffer = ''
        for x in range(0, len(v)):
            buffer = buffer + ''.join('%02x ' % (v[x]))
            if (x % 16 == 15):
                print(buffer)
                buffer = ''
        if (len(buffer) != 0):
            print(buffer)

    def show_state(self, why):
        groestl_state.dump(why, self.state)

    def clear(self):
        if self.sz <= 256:
            self.r = 10
            self.l = 512
            self.P = self.P512
            self.Q = self.Q512
        else:
            self.r = 14
            self.l = 1024
            self.P = self.P1024
            self.Q = self.Q1024
       
        self.mbytes = 0
        self.lbytes = self.l // 8
        self.window = []
        self.state = []
        self.set_iv()

    def set_iv(self):
        # start with zero state
        self.state = [0] * self.lbytes
        
        self.show_state('before-iv')
        
        # now write in radix-256 representation of sz
        p = len(self.state) - 1
        sz = self.sz
        while sz > 0:
            self.state[p] = sz % 256
            sz >>= 8
            p -= 1
            assert p != 0
        
        self.show_state('after-iv')

    def P512(self, v):
        return groestl_state.permutation(
                v,
                512,
                self.r,
                groestl_state.add_round_constant_p,
                (0, 1, 2, 3, 4, 5, 6, 7)
        )

    def Q512(self, v):
        return groestl_state.permutation(
                v,
                512,
                self.r,
                groestl_state.add_round_constant_q,
                (1, 3, 5, 7, 0, 2, 4, 6)
        )

    def P1024(self, v):
        return groestl_state.permutation(
                v,
                1024,
                self.r,
                groestl_state.add_round_constant_p,
                (0, 1, 2, 3, 4, 5, 6, 11)
        )

    def Q1024(self, v):
        return groestl_state.permutation(
                v,
                1024,
                self.r,
                groestl_state.add_round_constant_q,
                (1, 3, 5, 11, 0, 2, 4, 6)
        )
    
    @staticmethod
    def permutation(v, l, rounds, add_round_constant_fn, shift_bytes_indices):
        for i in range(rounds):
            v = add_round_constant_fn(v, i, l)
            v = groestl_state.sub_bytes(v)
            v = groestl_state.shift_bytes(v, shift_bytes_indices)
            v = groestl_state.mix_bytes(v)
        return v
    
    @staticmethod
    def add_round_constant_p(v, i, sz):
        szbytes = sz // 8
        constant = [0] * szbytes

        rows = 8
        cols = szbytes // rows

        for col in range(cols):
            constant[col * rows] = (col * 16) ^ i

        groestl_state.dump('add-round-constant(P-%d) for round %d' % (sz, i),
                           constant)

        return xor(constant, v)

    @staticmethod
    def add_round_constant_q(v, i, sz):
        szbytes = sz // 8
        constant = [0xff] * szbytes

        rows = 8
        cols = szbytes // 8

        for col in range(cols):
            constant[col * rows + rows - 1] = (0xff - col * 16) ^ i

        groestl_state.dump('add-round-constant(Q-%d) for round %d' % (sz, i),
                           constant)

        return xor(constant, v)

    @staticmethod
    def sub_bytes(v):
        groestl_state.dump('before-sub-bytes', v)
        v = [aes_sbox[y] for y in v]
        groestl_state.dump('after-sub-bytes', v)
        return v

    @staticmethod
    def rotl(v, n):
        """
        circularly rotate v left n places
        """
        assert n <= len(v)
        return v[n:] + v[:n]

    @staticmethod
    def shift_bytes(v, indices):
        rows = len(indices)
        cols = len(v) // rows
        v = list(v)

        def getrow(vv, i):
            return [vv[col * rows + i] for col in range(cols)]
        def setrow(vv, i, new):
            for col, n in enumerate(new):
                vv[col * rows + i] = n
        
        groestl_state.dump('shift-bytes(before)', v)

        for i, sigma in enumerate(indices):
            r = getrow(v, i)
            setrow(v, i, groestl_state.rotl(r, sigma))
        
        groestl_state.dump('shift-bytes(after)', v)

        return v

    @staticmethod
    def mix_bytes(v):
        def add(a, b):
            return a ^ b
        def mul(a, b):
            if a == 0 or b == 0:
                return 0

            x = gf256_log[a] + gf256_log[b]
            if x > 0xff:
                x -= 0xff

            return gf256_exp[x]

        assert 0x36 == mul(0xb6, 0x53)
        
        def matmul(A, B):
            """
            [ a b ] x [ x ] = [ ax + by ]
            [ c d ]   [ y ]   [ cx + dy ]
            """
            R = []

            #groestl_state.dump('matmul A', reduce(lambda x, y: x + y, A))
            #groestl_state.dump('matmul B', B)

            for row in A:
                n = []
                for i in range(len(row)):
                    n.append(mul(row[i], B[i]))

                R.append(reduce(add, n))
            
            #groestl_state.dump('matmul R', R)
            return R
        
        rows = 8
        cols = len(v) // rows
        v = list(v)

        groestl_state.dump('mix-bytes(before)', v)
        for col in range(cols):
            v[col * rows:col * rows + rows] = matmul(mixbytes_matrix,
                                                     v[col * rows:col * rows + rows])
        groestl_state.dump('mix-bytes(after)', v)
        return v

class groestl(base_hash):
    def __init__(self, sz, initial_pt = None):
        self.state = groestl_state(sz)
        base_hash.__init__(self, initial_pt)

    def update(self, pt):
        assert pt is not None
        self.state.add(pt)
        return self
        
    def finalise(self):
        # finalise cloned state, so we don't double-pad
        return self.state.clone().finalise()
