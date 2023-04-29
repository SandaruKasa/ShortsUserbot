pkgname=shorts-userbot
pkgver=0.r7.cb17b22
pkgrel=1
pkgdesc='A Telegram userbot that converts all YouTube Shorts link to normal videos'
arch=('any')
url="https://github.com/SandaruKasa/ShortsUserbot"
license=('APGL-3')
makedepends=('git')
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

package() {
  cd "${_git_folder}"
  mkdir -p "${pkgdir}/usr/"
  cp -rp systemd_files/ "${pkgdir}/usr/lib"
  install -Dm755 shorts_userbot.py -t "${pkgdir}/usr/lib/shorts_userbot/"
}
