package easymall.service;

import java.util.List;

import easymall.po.Cart;
import easymall.pojo.MyCart;

public interface CartService {
	//��ӹ��ﳵ
	public int addCart(Cart cart);
	//���ҹ��ﳵ�Ƿ���ڸ���Ʒ
	public Cart findCart(Cart cart);
	
	public int updateCart(Cart cart);
	
	public List<MyCart> showcart(int user_id);
	
	public void updateBuyNum(Cart cart);
	
	public void delCart(Integer cartID);
	
	//����cart ID���ҹ��ﳵ
	public MyCart findByCartID(Integer cartID);
}
