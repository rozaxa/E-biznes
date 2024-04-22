package main

import (
	"log"
	"net/http"
	"sync/atomic"

	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

type Product struct {
	ID    int     `json:"id"`
	Name  string  `json:"name"`
	Price float64 `json:"price"`
}

type Payment struct {
	ID     int     `json:"id"`
	Amount float64 `json:"amount"`
}

var (
	products []Product = []Product{
		{ID: 1, Name: "Product 1", Price: 9.99},
		{ID: 2, Name: "Product 2", Price: 4.99},
	}
	nextProductID int32 = 3
	payments      []Payment
	nextPaymentID int32 = 1
)

func main() {
	e := echo.New()
	e.Use(middleware.CORSWithConfig(middleware.CORSConfig{
		AllowOrigins: []string{"http://localhost:3000"},
		AllowMethods: []string{http.MethodGet, http.MethodPut, http.MethodPost, http.MethodDelete},
	}))

	e.GET("/products", getProducts)
	e.POST("/payments", postPayment)
	e.POST("/products", postProduct)
	e.GET("/payments", getPayments)

	e.Logger.Fatal(e.Start(":4000"))
}

func getProducts(c echo.Context) error {
	return c.JSON(http.StatusOK, products)
}

func postProduct(c echo.Context) error {
	newProduct := new(Product)
	if err := c.Bind(newProduct); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, "Invalid input")
	}
	newProduct.ID = int(atomic.AddInt32(&nextProductID, 1))
	products = append(products, *newProduct)
	log.Printf("New product added: %s, Price: %.2f", newProduct.Name, newProduct.Price)
	return c.JSON(http.StatusCreated, newProduct)
}

func postPayment(c echo.Context) error {
	payment := new(Payment)
	if err := c.Bind(payment); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, "Invalid input format")
	}
	if payment.Amount <= 0 {
		return echo.NewHTTPError(http.StatusBadRequest, "The payment amount must be greater than zero")
	}
	payment.ID = int(atomic.AddInt32(&nextPaymentID, 1))
	payments = append(payments, *payment)
	log.Printf("Payment received: %d, Amount: %.2f", payment.ID, payment.Amount)
	return c.JSON(http.StatusOK, payment)
}

func getPayments(c echo.Context) error {
	return c.JSON(http.StatusOK, payments)
}
