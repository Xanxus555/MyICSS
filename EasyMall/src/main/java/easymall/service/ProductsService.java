package easymall.service;

import java.util.List;
import java.util.Map;

import javax.servlet.http.HttpServletRequest;

import easymall.po.Category;
import easymall.po.Products;
import easymall.pojo.MyProducts;

public interface ProductsService {
	//
	public List<Category> allcategorys();
	//
	public List<Products> prodlist(Map<String,Object> map);
	//根据pid check
	public Products oneProduct(String pid);
	
	//根据分类查找商品
	public List<Products> proclass(Integer proclass);

	//添加商品
	public String save(MyProducts myproducts,HttpServletRequest request);
}
