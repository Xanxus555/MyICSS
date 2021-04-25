package easymall.dao;

import org.apache.ibatis.annotations.Mapper;
import org.springframework.stereotype.Repository;

import easymall.po.User;

@Repository
@Mapper
public interface UserDao {
	public User login(User user);
	//����û��Ƿ��Ѿ���ע��
	public User checkUsername(String username);
	//ע���û�
	public int regist(User user);
}
