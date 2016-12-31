# -*- coding: utf-8 -*-
#
#    bitcoinlib - Compact Python Bitcoin Library
#    Unit Tests for Wallet Class
#    © 2016 December - 1200 Web Development <http://1200wd.com/>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import unittest
import os

from bitcoinlib.db import DEFAULT_DATABASEDIR
from bitcoinlib.wallets import HDWallet

DATABASEFILE_UNITTESTS = DEFAULT_DATABASEDIR + 'bitcoinlib.unittest.sqlite'


class TestWallet(unittest.TestCase):

    def setUp(self):
        if os.path.isfile(DATABASEFILE_UNITTESTS):
            os.remove(DATABASEFILE_UNITTESTS)
        self.wallet = HDWallet.create(
            name='test_wallet_create',
            databasefile=DATABASEFILE_UNITTESTS)

    def test_wallet_create(self):
        self.assertTrue(isinstance(self.wallet, HDWallet))

    def test_wallet_info(self):
        self.assertIsNot(self.wallet.info(), "")

    def test_wallet_key_info(self):
        self.assertIsNot(self.wallet.main_key.info(), "")
        
    def test_wallet_create_account(self):
        new_account = self.wallet.new_account(account_id=100)
        self.assertEqual(new_account.depth, 3)
        self.assertEqual(new_account.key_wif[:4], 'xprv')
        self.assertEqual(new_account.path, "m/44'/0'/100'")

    def test_wallet_create_key(self):
        new_key = self.wallet.new_key(account_id=100)
        self.assertEqual(new_key.depth, 5)
        self.assertEqual(new_key.key_wif[:4], 'xprv')
        self.assertEqual(new_key.path, "m/44'/0'/100'/0/0")

    def test_wallet_import(self):
        keystr = 'tprv8ZgxMBicQKsPeWn8NtYVK5Hagad84UEPEs85EciCzf8xYWocuJovxsoNoxZAgfSrCp2xa6DdhDrzYVE8UXF75r2dKePy' \
                 'A7irEvBoe4aAn52'
        wallet_import = HDWallet.create(
            databasefile=DATABASEFILE_UNITTESTS,
            name='test_wallet_import',
            network='testnet',
            key=keystr)
        wallet_import.new_account(account_id=99)
        self.assertEqual(wallet_import.main_key.key_wif, keystr)
        self.assertEqual(wallet_import.main_key.address, u'n3UKaXBRDhTVpkvgRH7eARZFsYE989bHjw')
        self.assertEqual(wallet_import.main_key.path, 'm')

    def test_wallet_import_account(self):
        accountkey = 'tprv8h4wEmfC2aSckSCYa68t8MhL7F8p9xAy322B5d6ipzY5ZWGGwksJMoajMCqd73cP4EVRygPQubgJPu9duBzPn3QV' \
                     '8Y7KbKUnaMzx9nnsSvh'
        wallet_import = HDWallet.create(
            databasefile=DATABASEFILE_UNITTESTS,
            name='test_wallet_import_account',
            key=accountkey,
            network='testnet',
            account_id=99)
        self.assertEqual(wallet_import.main_key.key_wif, accountkey)
        self.assertEqual(wallet_import.main_key.address, u'mowRx2TNXTgRSUmepjqhx5C1TTigmHLGRh')
        self.assertEqual(wallet_import.main_key.path, "m/44'/1'/99'")

    def test_wallet_import_account_new_keys(self):
        accountkey = 'tprv8h4wEmfC2aSckSCYa68t8MhL7F8p9xAy322B5d6ipzY5ZWGGwksJMoajMCqd73cP4EVRygPQubgJPu9duBzPn3QV' \
                     '8Y7KbKUnaMzx9nnsSvh'
        wallet_import = HDWallet.create(
            databasefile=DATABASEFILE_UNITTESTS,
            name='test_wallet_import_account_new_key',
            key=accountkey,
            network='testnet',
            account_id=99)
        newkey = wallet_import.new_key(account_id=99)
        newkey_change = wallet_import.new_key_change(account_id=99, name='change')
        self.assertEqual(wallet_import.main_key.key_wif, accountkey)
        self.assertEqual(newkey.address, u'mfvFzusKPZzGBAhS69AWvziRPjamtRhYpZ')
        self.assertEqual(newkey.path, "m/44'/1'/99'/0/0")
        self.assertEqual(newkey_change.address, u'mkzpsGwaUU7rYzrDZZVXFne7dXEeo6Zpw2')
        self.assertEqual(newkey_change.path, "m/44'/1'/99'/1/0")

    def test_wallet_import_public_wallet(self):
        pubkey = 'tpubDDkyPBhSAx8DFYxx5aLjvKH6B6Eq2eDK1YN76x1WeijE8eVUswpibGbv8zJjD6yLDHzVcqWzSp2fWVFhEW9XnBssFqM' \
                 'wt9SrsVeBeqfBbR3'
        pubwal = HDWallet.create(
            databasefile=DATABASEFILE_UNITTESTS,
            name='test_wallet_import_public_wallet',
            key=pubkey,
            network='testnet',
            account_id=0)
        newkey = pubwal.new_key()
        self.assertEqual(newkey.address, u'mweZrbny4fmpCmQw9hJH7EVfkuWX8te9jc')

    def test_wallet_litecoin(self):
        accountkey = 'Ltpv71G8qDifUiNet6mn25D7GPAVLZeaFRWzDABxx5xNeigVpFEviHK1ZggPS1kbtegB3U2i8w6ToNfM5sdvEQPW' \
                     'tov4KWyQ5NxWUd3oDWXQb4C'
        wallet_import = HDWallet.create(
            databasefile=DATABASEFILE_UNITTESTS,
            name='test_wallet_litecoin',
            key=accountkey,
            network='litecoin')
        newkey = wallet_import.new_key()
        self.assertEqual(wallet_import.main_key.key_wif, accountkey)
        self.assertEqual(newkey.address, u'LPkJcpV1cmT8qLFmUApySBtxt7UWavoQmh')
        self.assertEqual(newkey.path, "m/44'/2'/0'/0/0")
