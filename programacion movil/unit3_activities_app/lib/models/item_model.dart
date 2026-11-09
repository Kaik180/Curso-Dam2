class ItemModel {
  final String id;
  final String title;
  final String category;
  final String description;
  final double price;
  final String imageUrl;
  final int rating;

  const ItemModel({
    required this.id,
    required this.title,
    required this.category,
    required this.description,
    required this.price,
    required this.imageUrl,
    this.rating = 5,
  });

  factory ItemModel.fromJson(Map<String, dynamic> json) {
    return ItemModel(
      id: json['id'] as String,
      title: json['title'] as String,
      category: json['category'] as String,
      description: json['description'] as String,
      price: (json['price'] as num).toDouble(),
      imageUrl: json['imageUrl'] as String,
      rating: json['rating'] as int? ?? 5,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'category': category,
      'description': description,
      'price': price,
      'imageUrl': imageUrl,
      'rating': rating,
    };
  }

  ItemModel copyWith({
    String? id,
    String? title,
    String? category,
    String? description,
    double? price,
    String? imageUrl,
    int? rating,
  }) {
    return ItemModel(
      id: id ?? this.id,
      title: title ?? this.title,
      category: category ?? this.category,
      description: description ?? this.description,
      price: price ?? this.price,
      imageUrl: imageUrl ?? this.imageUrl,
      rating: rating ?? this.rating,
    );
  }
}
