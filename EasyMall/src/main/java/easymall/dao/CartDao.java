package easymall.dao;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;
import org.springframework.stereotype.Repository;

import easymall.po.Cart;
import easymall.pojo.MyCart;

@Repository("cartDao")
@Mapper
public interface CartDao {
	//Ìí¼Ó¹ºÎï³µ
	public int addCart(Cart cart);
	
	public Cart findCart(Cart cart);
	
	public int updateCart(Cart cart);
	
	public List<MyCart> showcart(int user_id);
	
	public void updateBuyNum(Cart cart);
	
	public void delCart(Integer cartID);
	
	public MyCart findByCartID(Integer cartID);
}
