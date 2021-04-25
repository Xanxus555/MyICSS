package easymall.dao;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;
import org.springframework.stereotype.Repository;

import easymall.po.Orders;

@Repository("orderDao")
@Mapper
public interface OrderDao {
	
	public void addOrder(Orders myOrder);
	
	public List<Orders> findOrderByUserId(Integer user_id);

	public void delorder(String id);
	
	public List<Orders> findOrder();
	
	//Ö§¸¶¶©µ¥
	public void payorder(String id);
}
