import time
import random

from .utils import util as util
from .data import api as api




class QuarkTools:
    def __init__(self, cookie: str):
        self.api = api.Api(cookie)

    def store(self, url: str, to_dir_id="0", pdir_fid="0", second=False) -> list:
        """
        将链接下所有文件分别保存到目标文件夹，并为每个文件单独生成一个分享链接
        :param url: 分享链接
        :param to_dir_id: 目标文件夹id
        :param pdir_fid: 分享链接下级目录的id
        :param second: 是否保存二级目录到一级
        :return: 返回分享链接，文件名的列表
        """
        pwd_id = util.get_id_from_url(url)
        stoken = self.api.get_stoken(pwd_id)
        details = self.link_detail(pwd_id, stoken, pdir_fid)
        link_list = []
        if second:
            for detail in details:
                if 0 == detail.get("file_type"):
                    link_list.extend(self.store(url, to_dir_id=to_dir_id, pdir_fid=detail.get("fid"), second=False))
                else:
                    link_list.append(self.save_and_share(detail, pwd_id, stoken, to_dir_id))
                return link_list
        else:
            for detail in details:
                link_list.append(self.save_and_share(detail, pwd_id, stoken, to_dir_id))
            return link_list

    def save_and_share(self, detail, pwd_id, stoken, to_dir_id, ad=True):
        file_name = detail.get('title')
        file_id, share_fid_token, file_type = detail.get("fid"), detail.get("share_fid_token"), detail.get(
            "file_type")
        time.sleep(random.randint(2, 4))

        data = self.save_single_file(file_id, pwd_id, share_fid_token, stoken, to_dir_id)

        file_id = data.get("data").get("save_as").get("save_as_top_fids")[0]

        if ad:
            try:
                time.sleep(random.randint(2, 3))
                self.api.new_dir(f'更多游戏资源请添加VX公众号，game资源分享库', file_id)
            except:
                pass
        time.sleep(random.randint(2, 4))
        share_link = self.share_single_file(file_id, file_name)
        time.sleep(random.randint(2, 4))
        return [share_link, file_name,file_id]

    def share_single_file(self, file_id, file_name):

        share_task_id = self.api.share_task_id([file_id], file_name)
        share_id = self.api.task(share_task_id).get("data").get("share_id")
        share_link = self.api.get_share_link(share_id)

        return share_link

    def save_single_file(self, file_id, pwd_id, share_fid_token, stoken, to_dir_id):
        """
        保存单个文件到指定目录
        :param file_id: 文件ID
        :param pwd_id: 夸克网盘分享链接的pwd_id
        :param share_fid_token:
        :param stoken:
        :param to_dir_id: 保存到的文件夹ID
        :return:
        """
        task = self.api.save_task_id(pwd_id, stoken, [file_id], [share_fid_token], to_dir_id)
        data = self.api.task(task)
        return data

    def save_files(self, file_ids, pwd_id, share_fid_tokens, stoken, to_dir_id, pdir_fid=0):
        """
        保存单个文件到指定目录
        :param file_ids: 要保存的文件ID数组
        :param pwd_id: 夸克网盘分享链接的pwd_id
        :param share_fid_tokens: 分享token数组
        :param stoken:
        :param to_dir_id: 保存到的文件夹ID
        :param pdir_fid: 要保存的链接如果有上级目录，这里传上级目录ID
        :return:
        """
        task = self.api.save_task_id(pwd_id, stoken, file_ids, share_fid_tokens, to_dir_id, pdir_fid=pdir_fid)
        data = self.api.task(task)
        return data

    def link_detail(self, pwd_id, stoken, pdir_fid='0'):
        """
        获取分享链接数据详情，分页请求，若数据较多，可能需要比较久
        :param pwd_id:
        :param stoken:
        :param pdir_fid: 子文件夹ID
        :return: 链接下所有文件
        """
        have_next = True
        details = []
        page = 1
        while have_next:
            time.sleep(random.randint(2, 4))
            detail, have_next = self.api.detail(pwd_id, stoken, page=page, pdir_fid=pdir_fid)
            for item in detail:
                data = {
                    "title": item.get("file_name"),
                    "file_type": item.get("file_type"),
                    "fid": item.get("fid"),
                    "pdir_fid": item.get("pdir_fid"),
                    "share_fid_token": item.get("share_fid_token")
                }
                details.append(data)
        return details

    def delete_from_file(self, root_fid ):
        return self.api.delete_quark_file(root_fid)

    def store_from_file(self, link,root_dir='0', second=False):
        """
        保存分享链接
        :param in_file: 保存链接文件的文件
        :param out_file: 保存导出的链接的文件
        :param root_dir: 保存到的文件夹ID
        :param second: 是否保存二级目录到一级
        """
        # with (open("markdown.md", 'a') as markdown):
        data_list = self.store(link, to_dir_id=root_dir, second=second)
        for share_link, f_name,fid in data_list:
            print(fid)
            # markdown.write(f"{f_name.encode('utf-8').decode('utf-8')}:[夸克网盘]({share_link.encode('utf-8').decode('utf-8')})\n\n")
            return share_link,fid




#     print(link)
#     # name_fid='ff43ceb495744081889e76ee96dff9dc'
#
#     print(quark.delete_from_file(name_fid))
