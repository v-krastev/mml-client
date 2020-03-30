import unittest
from bin.song import Song


class TestSongAlbum(unittest.TestCase):
    def setUp(self) -> None:
        self.song = Song()

    def tearDown(self) -> None:
        del self.song

    def test_set_album_type(self):
        self.assertRaises(TypeError, self.song.set_album, album=3)
        self.assertRaises(TypeError, self.song.set_album, album=True)
        self.assertRaises(TypeError, self.song.set_album, album=None)

    def test_set_album_value(self):
        self.assertRaises(ValueError, self.song.set_album, album="")
        self.assertRaises(ValueError, self.song.set_album, album='')

    def test_set_album_correct(self):
        self.assertTrue(self.song.set_album("Name"))
        self.assertTrue(self.song.set_album("3"))
        self.assertTrue(self.song.set_album("None"))


class TestSongArtist(unittest.TestCase):
    def setUp(self) -> None:
        self.song = Song()

    def tearDown(self) -> None:
        del self.song

    def test_set_artist_type(self):
        self.assertRaises(TypeError, self.song.set_artist, artist=3)
        self.assertRaises(TypeError, self.song.set_artist, artist=True)
        self.assertRaises(TypeError, self.song.set_artist, artist=None)

    def test_set_artist_value(self):
        self.assertRaises(ValueError, self.song.set_artist, artist="")
        self.assertRaises(ValueError, self.song.set_artist, artist='')

    def test_set_artist_correct(self):
        self.assertTrue(self.song.set_artist("Name"))
        self.assertTrue(self.song.set_artist("3"))
        self.assertTrue(self.song.set_artist("None"))


class TestSongLength(unittest.TestCase):
    def setUp(self) -> None:
        self.song = Song()

    def tearDown(self) -> None:
        del self.song

    def test_set_length_type(self):
        self.assertRaises(TypeError, self.song.set_length, length=True)
        self.assertRaises(TypeError, self.song.set_length, length=object)

    def test_set_length_value(self):
        self.assertRaises(ValueError, self.song.set_length, length="-3")
        self.assertRaises(ValueError, self.song.set_length, length=-19.8)
        self.assertRaises(ValueError, self.song.set_length, length=-16)

    def test_set_length_correct(self):
        self.assertTrue(self.song.set_length("3"))
        self.assertTrue(self.song.set_length("5.14"))
        self.assertTrue(self.song.set_length(34))
        self.assertTrue(self.song.set_length(3.14))


class TestSongLengthPretty(unittest.TestCase):
    def setUp(self) -> None:
        self.song = Song()
        self.song.set_length(180)

    def tearDown(self) -> None:
        del self.song

    def test_length_pretty_180(self):
        self.song.set_length(180)
        self.assertEqual(self.song.length_pretty(hours=True, minutes=True, seconds=True), "0:03:00")
        self.assertEqual(self.song.length_pretty(minutes=True, seconds=True), "03:00")
        self.assertEqual(self.song.length_pretty(seconds=True), ":00")
        self.assertEqual(self.song.length_pretty(minutes=True), "03")
        self.assertEqual(self.song.length_pretty(hours=True), "0:")

    def test_length_pretty_221(self):
        self.song.set_length(221)
        self.assertEqual(self.song.length_pretty(hours=True, minutes=True, seconds=True), "0:03:41")
        self.assertEqual(self.song.length_pretty(minutes=True, seconds=True), "03:41")
        self.assertEqual(self.song.length_pretty(seconds=True), ":41")
        self.assertEqual(self.song.length_pretty(minutes=True), "03")
        self.assertEqual(self.song.length_pretty(hours=True), "0:")

    def test_length_pretty_4502(self):
        self.song.set_length(4502)
        self.assertEqual(self.song.length_pretty(hours=True, minutes=True, seconds=True), "1:15:02")
        self.assertEqual(self.song.length_pretty(minutes=True, seconds=True), "15:02")
        self.assertEqual(self.song.length_pretty(seconds=True), ":02")
        self.assertEqual(self.song.length_pretty(minutes=True), "15")
        self.assertEqual(self.song.length_pretty(hours=True), "1:")


class TestSongPath(unittest.TestCase):
    def setUp(self) -> None:
        self.song = Song()

    def tearDown(self) -> None:
        del self.song

    def test_set_path_type(self):
        self.assertRaises(TypeError, self.song.set_path, path=True)
        self.assertRaises(TypeError, self.song.set_path, path=-8.6)
        self.assertRaises(TypeError, self.song.set_path, path=object)

    def test_set_path_value(self):
        self.assertRaises(ValueError, self.song.set_path, path="True")
        self.assertRaises(ValueError, self.song.set_path, path="../data/songs")
        self.assertRaises(ValueError, self.song.set_path, path="../data/songs/empty.mp3")


class TestSongTitle(unittest.TestCase):
    def setUp(self) -> None:
        self.song = Song()

    def tearDown(self) -> None:
        del self.song

    def test_set_title_type(self):
        self.assertRaises(TypeError, self.song.set_title, title=3)
        self.assertRaises(TypeError, self.song.set_title, title=True)
        self.assertRaises(TypeError, self.song.set_title, title=None)

    def test_set_title_value(self):
        self.assertRaises(ValueError, self.song.set_title, title="")
        self.assertRaises(ValueError, self.song.set_title, title='')

    def test_set_title_correct(self):
        self.assertTrue(self.song.set_title("Name"))
        self.assertTrue(self.song.set_title("3"))
        self.assertTrue(self.song.set_title("None"))


if __name__ == "__main__":
    unittest.main()

    # song_test = TestSongMethods()
    # song_test.setUp()
    # song_test.test_set_album_correct()

    # unittest.main(verbosity=2)
    # suite = unittest.TestSuite()
    # suite.addTest(TestSongMethods)
    # suite.addTest(TestSongMethods("test_set_album_type"))
    # suite.addTests([TestSongMethods])
