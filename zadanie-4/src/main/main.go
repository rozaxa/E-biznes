package main

import (
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
	"net/http"
	"strconv"
	"sync"
)

type (
	product struct {
		ID    int     `json:"id"`
		Name  string  `json:"name"`
		Price float64 `json:"price"`
	}
)

var (
	products = map[int]*product{}
	seq      = 1
	lock     = sync.Mutex{}
)

func createProduct(c echo.Context) error {
	lock.Lock()
	defer lock.Unlock()
	p := &product{
		ID: seq,
	}
	if err := c.Bind(p); err != nil {
		return err
	}
	products[p.ID] = p
	seq++
	return c.JSON(http.StatusCreated, p)
}

func getProduct(c echo.Context) error {
	lock.Lock()
	defer lock.Unlock()
	id, _ := strconv.Atoi(c.Param("id"))
	if product, ok := products[id]; ok {
		return c.JSON(http.StatusOK, product)
	}
	return c.JSON(http.StatusNotFound, echo.Map{"message": "Product not found"})
}

func updateProduct(c echo.Context) error {
	lock.Lock()
	defer lock.Unlock()
	p := new(product)
	if err := c.Bind(p); err != nil {
		return err
	}
	id, _ := strconv.Atoi(c.Param("id"))
	if prod, ok := products[id]; ok {
		prod.Name = p.Name
		prod.Price = p.Price
		return c.JSON(http.StatusOK, prod)
	}
	return c.JSON(http.StatusNotFound, echo.Map{"message": "Product not found"})
}

func deleteProduct(c echo.Context) error {
	lock.Lock()
	defer lock.Unlock()
	id, _ := strconv.Atoi(c.Param("id"))
	if _, ok := products[id]; ok {
		delete(products, id)
		return c.NoContent(http.StatusNoContent)
	}
	return c.JSON(http.StatusNotFound, echo.Map{"message": "Product not found"})
}

func getAllProducts(c echo.Context) error {
	lock.Lock()
	defer lock.Unlock()
	return c.JSON(http.StatusOK, products)
}

func main() {
	e := echo.New()

	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	e.GET("/products", getAllProducts)
	e.POST("/products", createProduct)
	e.GET("/products/:id", getProduct)
	e.PUT("/products/:id", updateProduct)
	e.DELETE("/products/:id", deleteProduct)

	e.Logger.Fatal(e.Start(":1323"))
}
