package easymall.service;

import java.util.List;

import easymall.po.Cart;
import easymall.pojo.MyCart;

public interface CartService {
	//添加购物车
	public int addCart(Cart cart);
	//查找购物车是否存在该商品
	public Cart findCart(Cart cart);
	
	public int updateCart(Cart cart);
	
	public List<MyCart> showcart(int user_id);
	
	public void updateBuyNum(Cart cart);
	
	public void delCart(Integer cartID);
	
	//根据cart ID查找购物车
	public MyCart findByCartID(Integer cartID);
}
