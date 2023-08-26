pkgname=shorts-userbot
pkgver=0.r11.c1b857c
pkgrel=1
pkgdesc='A Telegram userbot that converts all YouTube Shorts link to normal videos'
arch=('any')
url="https://github.com/SandaruKasa/ShortsUserbot"
license=('custom')
makedepends=('git' "python-build" "python-installer" "python-wheel" "python-setuptools")
depends=('python>=3.10' 'python-pyrogram' 'systemd')
_git_folder="${pkgname%-git}"
source=("${_git_folder}::git+${url}")
sha256sums=(SKIP)

pkgver() {
  cd "${_git_folder}"
  printf "%s.r%s.%s" \
    "0" \
    "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

build() {
  cd "${_git_folder}"
  python -m build --wheel --no-isolation
}

package() {
  cd "${_git_folder}"
  python -m installer --destdir="$pkgdir" dist/*.whl
  cp -rp systemd_files/* "${pkgdir}/usr/lib"
  install -Dm644 LICENSE "${pkgdir}/usr/share/licenses/$pkgname/LICENSE"
}
