package easymall.dao;

import org.apache.ibatis.annotations.Mapper;
import org.springframework.stereotype.Repository;

import easymall.po.User;

@Repository
@Mapper
public interface UserDao {
	public User login(User user);
	//检查用户是否已经被注册
	public User checkUsername(String username);
	//注册用户
	public int regist(User user);
}
