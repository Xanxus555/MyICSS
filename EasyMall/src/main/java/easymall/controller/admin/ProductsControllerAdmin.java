package easymall.controller.admin;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.RequestMapping;

import easymall.po.Category;
import easymall.po.OrderItem;
import easymall.po.Orders;
import easymall.po.Products;
import easymall.pojo.MyProducts;
import easymall.pojo.OrderInfo;
import easymall.service.OrderService;
import easymall.service.ProductsService;

@Controller("productsControllerAdmin")
@RequestMapping("/admin")
public class ProductsControllerAdmin {
	@Autowired
	private ProductsService productsService;
	@Autowired
	 private OrderService orderService;
	@RequestMapping("/addprod")
	public String addprod(Model model){
		
		List<Category> categorys = productsService.allcategorys();
		model.addAttribute("categorys",categorys);
		model.addAttribute("myproducts",new MyProducts());
		return "admin/add_prod";
	}
	
	@RequestMapping("/manageorder")
	public String manageorder(Model model)
	{
		List<OrderInfo> orderInfoList=findOrderInfo();	
		model.addAttribute("orderInfos", orderInfoList);
		return "admin/manage_order";
	}
	
	@RequestMapping("/save")
	public String save(@ModelAttribute MyProducts myproducts,
			HttpServletRequest request,Model model)
			throws Exception{
		String msg=productsService.save(myproducts,request);
		model.addAttribute("msg",msg);
		return "redirect:/admin/addprod";
	}
	
	@RequestMapping("/findOrderInfoByUserId")
	 public List<OrderInfo> findOrderInfo() {
	  List<OrderInfo> orderInfoList = new ArrayList<OrderInfo>();
	  List<Orders> orderList = orderService.findOrder();
	  for(Orders order:orderList) {
	   List<OrderItem> orderitems=orderService.orderitem(order.getId());
	   Map<Products,Integer> map=new HashMap<Products,Integer>();
	   for(OrderItem orderItem:orderitems) {
	    Products product=productsService.oneProduct(orderItem.getProduct_id());
	    map.put(product, orderItem.getBuynum());
	   }
	   OrderInfo orderInfo=new OrderInfo();
	   orderInfo.setOrder(order);
	   orderInfo.setMap(map);
	   orderInfoList.add(orderInfo);
	  }
	  return orderInfoList;
	 }

}
