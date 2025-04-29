title_vnexpress = [
    'thoi-su', 
    'the-gioi', 
    'kinh-doanh', 
    'khoa-hoc-cong-nghe', 
    'bat-dong-san', 
    'suc-khoe', 
    'the-thao', 
    'giai-tri', 
    'phap-luat', 
    'giao-duc', 
    'doi-song', 
    'oto-xe-may', 
    'du-lich'
]

title_vietnamnet = {
    'chinh-tri': ['su-kien', 'xay-dung-dang', 'doi-ngoai', 'ban-luan', 'ky-nguyen-moi-cua-dan-toc', 'quoc-phong', 'nghi-quyet-57'],
    'thoi-su': ['dan-sinh', 'giao-thong', 'tin-nong', 'do-thi'],
    'kinh-doanh': ['net-zero', 'tai-chinh', 'dau-tu', 'thi-truong', 'doanh-nhan', 'tu-van-tai-chinh'],
    'dan-toc-ton-giao': ['tin-tuc', 'sac-mau-viet-nam', 'chinh-sach-phat-trien', 'nhan-vat', 'doi-song-ton-giao', 'tu-van'],
    'the-thao': ['bong-da-viet-nam', 'bong-da-quoc-te', 'tin-chuyen-nhuong', 'hau-truong', 'cac-mon-khac'],
    'giao-duc': ['nha-truong', 'chan-dung', 'goc-phu-huynh', 'tuyen-sinh', 'du-hoc', 'hoc-tieng-anh', 'khoa-hoc', 'ai-contest'],
    'the-gioi': ['binh-luan-quoc-te', 'chan-dung', 'ho-so', 'the-gioi-do-day', 'viet-nam-va-the-gioi', 'quan-su'],
    'doi-song': ['gia-dinh', 'chuyen-la', 'am-thuc', 'gioi-tre', 'meo-vat'],
    'van-hoa-giai-tri': ['the-gioi-sao', 'nhac', 'phim-truyen-hinh', 'sach', 'my-thuat-san-khau', 'di-san'],
    'suc-khoe': ['suc-khoe-24h', 'lam-dep', 'tu-van-suc-khoe', 'dan-ong', 'benh'],
    'cong-nghe': ['thi-truong', 'chuyen-doi-so', 'ha-tang-so', 'an-ninh-mang', 'san-pham', 'ai'],
    'phap-luat': ['ho-so-vu-an', 'tu-van-phap-luat', 'ky-su-phap-dinh'],
    'oto-xe-may': ['xe-moi', 'kham-pha', 'sau-tay-lai', 'dien-dan', 'tu-van', 'danh-gia-xe', 'gia-xe'],
    'bat-dong-san': ['du-an', 'noi-that', 'kinh-nghiem-tu-van', 'thi-truong', 'nha-dep', 'kim-oanh-group'],
    'du-lich': ['di-dau-choi-di', 'an-uong', 'ngu-nghi']
}


title_dantri = {
    'xa-hoi': ['chinh-tri', 'hoc-tap-bac', 'ky-nguyen-moi', 'moi-truong', 'giao-thong', 'nong-tren-mang'],
    'the-gioi': ['quan-su', 'phan-tich-binh-luan', 'the-gioi-do-day', 'kieu-bao'],
    'kinh-doanh': ['tai-chinh', 'chung-khoan', 'doanh-nghiep', 'khoi-nghiep', 'tieu-dung'],
    'bat-dong-san': ['du-an', 'thi-truong', 'nha-dat', 'nhip-song-do-thi', 'song-xanh', 'noi-that'],
    'the-thao': ['bong-da', 'pickleball', 'tennis', 'golf', 'vo-thuat-cac-mon-khac', 'hau-truong', 'the-thao-suc-ben'],
    'suc-khoe': ['ung-thu', 'song-khoe', 'ngoai-than-kinh-cot-song', 'kien-thuc-gioi-tinh', 'tu-van', 'khoe-dep'],
    'noi-vu': ['chinh-sach', 'to-chuc-bo-may', 'tien-luong', 'cong-so'],
    'giai-tri': ['hau-truong', 'sach-hay', 'dien-anh', 'am-nhac', 'thoi-trang', 'my-thuat-san-khau', 'hat-giong-tam-hon'],
    'o-to-xe-may': ['thi-truong-xe', 'xe-dien', 'danh-gia', 'cong-dong-xe', 'kinh-nghiem-tu-van'],
    'cong-nghe': ['ai-internet', 'an-ninh-mang', 'gia-dung-thong-minh', 'san-pham-cong-dong'],
    'giao-duc': ['goc-phu-huynh', 'khuyen-hoc', 'guong-sang', 'giao-duc-nghe-nghiep', 'du-hoc', 'tuyen-sinh'],
    'viec-lam': ['nhan-luc-moi', 'lam-giau', 'an-sinh', 'chuyen-nghe'],
    'phap-luat': ['ho-so-vu-an', 'phap-dinh'],
    'du-lich': ['tin-tuc', 'kham-pha', 'mon-ngon-diem-dep', 'tour-hay-khuyen-mai', 'video-anh'],
    'doi-song': ['cong-dong', 'thuong-luu', 'nha-dep', 'gioi-tre', 'cho-online'],
    'tinh-yeu': ['chuyen-cua-toi', 'gia-dinh', 'tinh-yeu'],
    'khoa-hoc': ['the-gioi-tu-nhien', 'vu-tru', 'kham-pha', 'khoa-hoc-doi-song']
}


def get_url_list(title, begin_page, end_page):
    url_list = []

    if title == 'vnexpress':
        for category in title_vnexpress:
            for i in range(begin_page, end_page+1):
                url_list.append(f"https://vnexpress.net/{category}-p{i}")
        return url_list

    if title == 'dantri':
        for category in title_dantri.keys():
            for subcategory in title_dantri[category]:
                for i in range(begin_page, end_page+1):
                    url_list.append(f"https://dantri.com.vn/{category}/{subcategory}/trang-{i}.htm")
        return url_list
    
    if title == 'vietnamnet':
        for category in title_vietnamnet.keys():
            for subcategory in title_vietnamnet[category]:
                for i in range(begin_page, end_page+1):
                    url_list.append(f"https://vietnamnet.vn/{category}/{subcategory}-page{i}")
        return url_list
    
    return url_list