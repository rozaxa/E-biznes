package controllers

import play.api.libs.json._
import play.api.mvc._

import javax.inject._

import models.Product

@Singleton
class ProductController @Inject()(val controllerComponents: ControllerComponents) extends BaseController {
  var products = Seq(
    Product(1, "Product_1", 17 ),
    Product(2, "Product_2", 25 ),
    Product(3, "Product_3", 30 )
  )

  implicit val productWrites: Writes[Product] = new Writes[Product] {
    def writes(product: Product): JsObject = Json.obj(
      "id" -> product.id,
      "name" -> product.name,
      "price" -> product.price
    )
  }

  def getAllProducts = Action {
    val json = Json.toJson(products)
    Ok(Json.prettyPrint(json))
  }

}
