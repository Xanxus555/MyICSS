package easymall.service;

import easymall.po.User;

public interface UserService {
	public User login(User user);
	//����û��Ƿ��Ѿ���ע��
	public Boolean checkUsername(String username);
	//ע���û�
	public int regist(User user);
}
